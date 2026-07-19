#!/usr/bin/env bash
# Trace — update an already-deployed instance to the latest main.
# Run ON the instance:  sudo bash Trace/deploy/update.sh   (any cwd works)
#
# Counterpart to deploy_alibaba.sh (the one-shot install): pulls main, syncs
# deps, runs the offline test suite as an update gate, restarts the service.
# The per-project decision stores (kb/<project>/trace.db, gitignored) are
# PERSISTENT by design — they survive this update untouched.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$REPO_DIR/Trace"
SERVICE=trace-bubble

cd "$REPO_DIR"
echo "==> pulling latest main into $REPO_DIR"
git fetch origin main
git checkout main
git pull --ff-only origin main || {
  echo "!! fast-forward pull failed — the instance has local commits/edits."
  echo "   Inspect with 'git status' and 'git log origin/main..' before forcing anything."
  exit 1
}

echo "==> syncing dependencies"
"$REPO_DIR/.venv/bin/pip" install --quiet -r "$APP_DIR/requirements.txt"

echo "==> running the offline test suite as an update gate"
(cd "$APP_DIR" && "$REPO_DIR/.venv/bin/python" -m pytest -q)

echo "==> restarting $SERVICE"
systemctl restart "$SERVICE"
sleep 1
systemctl --no-pager --lines=5 status "$SERVICE" || true

IP=$(curl -s --max-time 3 http://100.100.100.200/latest/meta-data/eipv4 || hostname -I | awk '{print $1}')
echo
echo "==> updated. bubble: http://$IP"
echo "    Decision stores persist in kb/<project>/trace.db across updates/restarts."
echo "    To reset one project to the demo seed:"
echo "      rm $REPO_DIR/kb/<project>/trace.db*  && systemctl restart $SERVICE"
echo "    Logs:  journalctl -u $SERVICE -f"
