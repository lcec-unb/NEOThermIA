#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# NEOThermIA launcher
# - Creates/uses local Python venv
# - Installs dependencies from requirements.txt
# - Runs main.py
# - Opens local web UI
# ============================================================================
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

VENV_DIR="${PROJECT_DIR}/.venv"
REQ_FILE="${PROJECT_DIR}/requirements.txt"
MAIN_FILE="${PROJECT_DIR}/main.py"
URL="http://127.0.0.1:8051/"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║ 🚀  NEOThermIA — launcher                                                    ║"
echo "║ 🔧  Ambiente: venv local (.venv)                                             ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# --- sanity checks
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ python3 não encontrado. Instale Python 3 e tente novamente."
  exit 1
fi

if [[ ! -f "$MAIN_FILE" ]]; then
  echo "❌ main.py não encontrado em: $MAIN_FILE"
  exit 1
fi

if [[ ! -f "$REQ_FILE" ]]; then
  echo "❌ requirements.txt não encontrado em: $REQ_FILE"
  exit 1
fi

# --- ensure venv module exists
if ! python3 -c "import venv" >/dev/null 2>&1; then
  echo "❌ Módulo venv indisponível no seu Python."
  echo "   No Ubuntu/Debian, normalmente resolve com:"
  echo "   sudo apt-get install -y python3-venv"
  exit 1
fi

# --- create venv if missing
if [[ ! -d "$VENV_DIR" ]]; then
  echo "📦 Criando ambiente virtual em: $VENV_DIR"
  python3 -m venv "$VENV_DIR"
else
  echo "📦 Ambiente virtual já existe em: $VENV_DIR"
fi

# --- activate venv
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "✅ venv ativo: $(python -c 'import sys; print(sys.executable)')"

# --- upgrade pip tooling
echo "⬆️  Atualizando pip/setuptools/wheel..."
python -m pip install --upgrade pip setuptools wheel >/dev/null

# --- install requirements (correct usage is -r)
echo "📚 Instalando dependências de requirements.txt..."
python -m pip install -r "$REQ_FILE"

# --- start server
echo ""
echo "▶️  Executando: python main.py"
echo "🌐 A interface será aberta em: $URL"
echo ""

# Run in background so we can open browser immediately
python "$MAIN_FILE" &
APP_PID=$!

# --- wait a bit for server to come up (simple loop; no extra deps)
echo "⏳ Aguardando servidor subir..."
for _ in {1..50}; do
  if command -v curl >/dev/null 2>&1; then
    if curl -sSf "$URL" >/dev/null 2>&1; then
      break
    fi
  else
    # no curl: just sleep a bit and assume it's fine
    sleep 0.2
    break
  fi
  sleep 0.2
done

# --- open browser
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 || true
elif command -v gio >/dev/null 2>&1; then
  gio open "$URL" >/dev/null 2>&1 || true
else
  echo "ℹ️  Não achei xdg-open/gio. Abra manualmente: $URL"
fi

echo ""
echo "✅ NEOThermIA em execução (PID: $APP_PID)."
echo "🛑 Para encerrar: pressione Ctrl+C ou rode: kill $APP_PID"
echo ""

# Bring process to foreground so Ctrl+C works as expected
wait "$APP_PID"
