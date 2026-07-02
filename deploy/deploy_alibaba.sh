#!/usr/bin/env bash
# Trace — one-shot deploy onto an Alibaba Cloud ECS instance (Ubuntu 22.04/24.04).
# Run ON the instance, from the repo root:  sudo bash deploy/deploy_alibaba.sh
#
# What it does: python venv + deps, then installs and starts a systemd service
# serving the Trace bubble (bubble.py) on 0.0.0.0:8765.
# Prereqs: the repo is on the instance; Trace/.env contains DASHSCOPE_API_KEY
# (put it there yourself — never commit it); port 8765 open in the security group.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$REPO_DIR/Trace"
SERVICE=trace-bubble

echo "==> Trace deploy from $REPO_DIR"

if [ ! -f "$APP_DIR/.env" ]; then
  echo "!! $APP_DIR/.env not found. Create it first with a single line:"
  echo "   DASHSCOPE_API_KEY=sk-..."
  echo "   (the bubble UI still serves without it, but /ask answers will fail)"
fi

apt-get update -qq
apt-get install -y -qq python3-venv python3-pip >/dev/null

python3 -m venv "$REPO_DIR/.venv"
"$REPO_DIR/.venv/bin/pip" install --quiet --upgrade pip
"$REPO_DIR/.venv/bin/pip" install --quiet -r "$APP_DIR/requirements.txt"

echo "==> running the offline test suite as a deployment gate"
(cd "$APP_DIR" && "$REPO_DIR/.venv/bin/python" -m pytest -q)

cat > /etc/systemd/system/$SERVICE.service <<EOF
[Unit]
Description=Trace ambient bubble (Qwen Cloud hackathon demo)
After=network.target

[Service]
WorkingDirectory=$APP_DIR
Environment=TRACE_HOST=0.0.0.0
Environment=TRACE_PORT=8765
ExecStart=$REPO_DIR/.venv/bin/python bubble.py --no-browser
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now $SERVICE

sleep 1
systemctl --no-pager --lines=5 status $SERVICE || true
IP=$(curl -s --max-time 3 http://100.100.100.200/latest/meta-data/eipv4 || hostname -I | awk '{print $1}')
echo
echo "==> Trace bubble is up:  http://$IP:8765"
echo "    This URL is the judges' testing-access link (rules §4)."
echo "    Logs:  journalctl -u $SERVICE -f"
