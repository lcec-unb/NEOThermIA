# MLP_KerasPredict.py
import os
import warnings
import pickle
import joblib
import numpy as np
from tensorflow.keras.models import load_model

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# =========================
#  Pipeline classes
# =========================
class KerasPipelineModel:
    def __init__(self, model_path: str, scalerX_path: str, scalerY_path: str):

        self.model = load_model(model_path)

        with open(scalerX_path, "rb") as file:
            self.scalerX = pickle.load(file)

        with open(scalerY_path, "rb") as file:
            self.scalerY = pickle.load(file)

    @staticmethod
    def _ensure_2d(X):
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        return X

    def predict(self, input_data):
        X = self._ensure_2d(input_data)
        X_scaled = self.scalerX.transform(X)

        y_pred_scaled = self.model.predict(X_scaled, verbose=0)

        y_pred = self.scalerY.inverse_transform(y_pred_scaled)
        return y_pred

_PIPELINE_CACHE = {}

def _get_pipeline(model_path: str = "surrogate_model/Keras_MLP_Surrogate.keras",
                  scalerX_path: str = "surrogate_model/scalerX.pkl",
                  scalerY_path: str = "surrogate_model/scalerY.pkl"):

    key = (model_path, scalerX_path, scalerY_path)
    if key in _PIPELINE_CACHE:
        return _PIPELINE_CACHE[key]

    pipeline = KerasPipelineModel(model_path, scalerX_path, scalerY_path)

    _PIPELINE_CACHE[key] = pipeline
    return pipeline


def PredictValues(input_data, Tensor=False):
    pipeline_model = _get_pipeline()

    ypred = pipeline_model.predict(input_data)  # sempre 2D

    if Tensor:
        return ypred
    else:
        # Garante 1D (n_outputs,)
        return np.asarray(ypred, dtype=float).reshape(ypred.shape[0], -1)[0]
