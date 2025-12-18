# =====================================================================
# AI4HyperTherm - NSGA-II Optimization (com vf e r_nm fixos)
# =====================================================================

import numpy as np
import pandas as pd
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from surrogate_model.MLP_KerasPredict import PredictValues


def run_hyperthermia_optimization(
    tumor_mm=7.0,
    e=0.7,
    vf_pct=4.0,
    r_nm=8.0,
    tc_max=46.5,
    tavg_min=40.0,   # <- agora o nome bate com o callback/layout
    pop_size=80,
    n_gen=100
):
    """
    Executa a otimização considerando vf e r_nm fixos.

    Restrições clínicas:
        - TC <= tc_max     (temperatura central máxima permitida)
        - TMIN >= tavg_min (aqui tavg_min é o limiar mínimo da menor temperatura no tumor)
    """

    # ============================================================== #
    # Classe do problema
    # ============================================================== #
    class HyperthermiaOptimization(Problem):
        def __init__(self):
            super().__init__(
                n_var=2,          # apenas h e f
                n_obj=3,          # min S_TIME, min TSTD, max TAVG
                n_constr=2,       # TC ≤ tc_max, TMIN ≥ tavg_min
                xl=np.array([1500, 100000], dtype=float),   # limites inferiores (h, f)
                xu=np.array([4000, 300000], dtype=float),   # limites superiores
                elementwise_evaluation=False,
            )

        def _evaluate(self, X, out, *args, **kwargs):
            h = X[:, 0]
            f = X[:, 1]
            n = X.shape[0]

            # Parâmetros fixos definidos pelo médico
            vf_frac = np.full(n, vf_pct / 100.0)
            r_m     = np.full(n, r_nm * 1e-9)
            tumor_m = np.full(n, tumor_mm * 1e-3)
            e_vec   = np.full(n, e)

            input_data = np.column_stack([vf_frac, h, f, r_m, tumor_m, e_vec]).astype(np.float32)
            outputs = PredictValues(input_data, Tensor=True)

            tc   = outputs[:, 0]
            st   = outputs[:, 1]
            tmin = outputs[:, 2]
            tavg = outputs[:, 3]
            tstd = outputs[:, 4]
            sar  = outputs[:, 5]
            raf_mm = outputs[:, 6] * 1000.0

            # Objetivos
            f1 = st
            f2 = tstd
            f3 = -tavg

            # Restrições (TC ≤ tc_max e TMIN ≥ tavg_min)
            g1 = tc - tc_max
            g2 = tavg_min - tmin

            out["F"] = np.column_stack([f1, f2, f3])
            out["G"] = np.column_stack([g1, g2])

            viaveis = ((g1 <= 0) & (g2 <= 0)).sum()
            print(
                f"[DEBUG] {n:3d} aval. | ⌀TAVG={np.mean(tavg):.2f} °C | "
                f"TCmax={np.max(tc):.2f} °C | TMIN(min)={np.min(tmin):.2f} °C | Viáveis={viaveis}/{n}"
            )

    # ============================================================== #
    # Execução
    # ============================================================== #
    print(
        f"\n=== Otimização: tumor={tumor_mm:.1f} mm | e={e:.2f} | "
        f"vf={vf_pct:.1f}% | r={r_nm:.1f} nm ==="
    )

    problem = HyperthermiaOptimization()
    algorithm = NSGA2(pop_size=pop_size)

    res = minimize(problem, algorithm, termination=('n_gen', n_gen), verbose=True)

    # ============================================================== #
    # Filtragem de soluções viáveis
    # ============================================================== #
    if getattr(res, "G", None) is not None:
        feasible_mask = np.all(res.G <= 0, axis=1)
    else:
        feasible_mask = np.ones(res.F.shape[0], dtype=bool)

    Xf = res.X[feasible_mask]
    if len(Xf) == 0:
        print("⚠️ Nenhuma solução viável encontrada.")
        return pd.DataFrame(), None

    # ============================================================== #
    # Reavalia para obter métricas físicas completas
    # ============================================================== #
    h = Xf[:, 0]
    f = Xf[:, 1]
    n = len(Xf)

    vf_frac = np.full(n, vf_pct / 100.0)
    r_m     = np.full(n, r_nm * 1e-9)
    tumor_m = np.full(n, tumor_mm * 1e-3)
    e_vec   = np.full(n, e)

    input_data = np.column_stack([vf_frac, h, f, r_m, tumor_m, e_vec]).astype(np.float32)
    outputs = PredictValues(input_data, Tensor=True)

    tc   = outputs[:, 0]
    st   = outputs[:, 1]
    tmin = outputs[:, 2]
    tavg = outputs[:, 3]
    tstd = outputs[:, 4]
    sar  = outputs[:, 5]
    raf_mm = outputs[:, 6] * 1000.0

    df = pd.DataFrame({
        "vf(%)":   np.full(n, vf_pct),
        "r_nm":    np.full(n, r_nm),
        "H(A/m)":  h,
        "f(Hz)":   f,
        "TC(°C)":  tc,
        "TAVG(°C)": tavg,
        "TMIN(°C)": tmin,
        "TSTD":    tstd,
        "S_TIME(s)": st,
        "SAR(W/kg)": sar,
        "RAF(mm)":  raf_mm,
    }).sort_values(by=["S_TIME(s)", "TSTD"]).reset_index(drop=True)

    pareto_data = {"F": res.F, "X": res.X, "feasible_mask": feasible_mask}

    print(f"✅ {len(df)} soluções viáveis encontradas.")
    return df, pareto_data
