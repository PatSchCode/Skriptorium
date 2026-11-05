#!/usr/bin/env bash
# Zweck: Richtet eine Session des Coding-Agents für Skriptorium ein – feste Werkzeug-
#   Versionen (uv, Python, Node), Projekt-Abhängigkeiten und den Pre-Commit-Hook (ADR-015,
#   ADR-026). Aufgerufen als SessionStart-Hook aus .claude/settings.json.
# Voraussetzungen: bash 3.2+, curl, tar (mit xz), sha256sum, python3 mit venv, git;
#   ENV: CLAUDE_CODE_REMOTE (nur bei "true" aktiv), CLAUDE_PROJECT_DIR, CLAUDE_ENV_FILE
#   (beide vom Werkzeug gesetzt); Netz zu pypi.org, nodejs.org, registry.npmjs.org.
# Plattformen: Linux x86_64 (nur Cloud-Session, CLAUDE_CODE_REMOTE=true) und macOS arm64
#   (lokale Session auf dem Mac des Eigentümers, ADR-026). Sonst ohne Wirkung; Windows nicht
#   unterstützt – dort entwickelt niemand (docs/project-context.md Abschnitt 3).
# Idempotenz: ja – vorhandene Werkzeuge mit passender Version werden nicht neu geladen;
#   `uv sync`, `npm install` und `pre-commit install` sind wiederholbar.
# Reproduzierbarkeit: Werkzeug-Versionen fest, Node-Archiv per SHA-256 geprüft,
#   Abhängigkeiten aus uv.lock und package-lock.json; wiederholte Aufrufe ergeben denselben Stand.
set -euo pipefail

platform="$(uname -s)-$(uname -m)"
if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ] && [ "${platform}" = "Linux-x86_64" ]; then
  node_platform="linux-x64"
  node_sha256="6170b2d474e1c626f43cff3adc118df9fe3b573258a4fc3d850c8dbc6b079bbd"
elif [ "${platform}" = "Darwin-arm64" ]; then
  node_platform="darwin-arm64"
  node_sha256="18830bf448fe187c650dc28c98aa8c968ed1d40b6dd032c081e70a384a1bf660"
else
  exit 0
fi

UV_VERSION="0.12.19"
PYTHON_VERSION="3.14.7"
NODE_VERSION="26.12.1"

project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
tools_dir="${HOME}/.cache/skriptorium-tools"
uv_venv="${tools_dir}/uv-${UV_VERSION}"
node_dir="${tools_dir}/node-v${NODE_VERSION}-${node_platform}"
mkdir -p "${tools_dir}"

# Die Umgebung setzt UV_NATIVE_TLS, das uv 0.12 als abgekündigt meldet; Ersatz UV_SYSTEM_CERTS.
unset UV_NATIVE_TLS
export UV_SYSTEM_CERTS=1

if [ ! -x "${uv_venv}/bin/uv" ] || [ "$("${uv_venv}/bin/uv" --version | cut -d' ' -f2)" != "${UV_VERSION}" ]; then
  rm -rf "${uv_venv}"
  python3 -m venv "${uv_venv}"
  "${uv_venv}/bin/pip" install --quiet --disable-pip-version-check "uv==${UV_VERSION}"
fi

if [ ! -x "${node_dir}/bin/node" ]; then
  archive="${tools_dir}/node-v${NODE_VERSION}-${node_platform}.tar.xz"
  curl -sSfL -o "${archive}" "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-${node_platform}.tar.xz"
  # Vergleich in der Shell: GNU- und BSD-sha256sum (macOS) teilen keine Prüf-Option.
  if [ "$(sha256sum "${archive}" | cut -d' ' -f1)" != "${node_sha256}" ]; then
    echo "Prüfsumme von ${archive} falsch" >&2
    rm -f "${archive}"
    exit 1
  fi
  tar -xJf "${archive}" -C "${tools_dir}"
  rm -f "${archive}"
fi

export PATH="${uv_venv}/bin:${node_dir}/bin:${PATH}"

cd "${project_dir}"
uv python install "${PYTHON_VERSION}"
uv sync --frozen --python "${PYTHON_VERSION}"
npm install --no-audit --no-fund
uv run --frozen pre-commit install

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export PATH=\"${uv_venv}/bin:${node_dir}/bin:\${PATH}\""
    echo "unset UV_NATIVE_TLS"
    echo "export UV_SYSTEM_CERTS=1"
  } >> "${CLAUDE_ENV_FILE}"
fi
