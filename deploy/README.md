# Deploying Trace on Alibaba Cloud

**Why this exists:** the official rules ([docs/12](../docs/12-devpost-official-rules.md) §4) make Alibaba Cloud deployment **mandatory**: *"You must demonstrate that the backend is running on Alibaba Cloud. Proof must be a link to a code file in their code repo that demonstrates use of Alibaba Cloud services and APIs."* The same deployment doubles as the required **testing-access link** (free judge access through 31 Jul).

## Proof of Alibaba Cloud usage (for the Devpost form)

Link these repo files on the submission form — they demonstrate Alibaba Cloud services/APIs directly:

- [`Trace/capture.py`](../Trace/capture.py) — Qwen (qwen-plus) function-calling on the Alibaba Cloud Model Studio **Singapore DashScope endpoint** (`dashscope-intl.aliyuncs.com`)
- [`Trace/court.py`](../Trace/court.py) — three Qwen roles on the same endpoint
- [`Trace/recall.py`](../Trace/recall.py) — Qwen answer synthesis on the same endpoint
- [`deploy/deploy_alibaba.sh`](deploy_alibaba.sh) — the ECS deployment itself

## Steps (≈20 minutes, human parts marked 👤)

1. 👤 **Create the ECS instance** — Alibaba Cloud console → ECS → Create:
   region **Singapore (ap-southeast-1)** (same region as the DashScope endpoint),
   Ubuntu 22.04 or 24.04, smallest spec is fine (2 vCPU / 2 GB, e.g. ecs.t6),
   assign a public IP. In the **security group**, allow inbound **TCP 80** (standard HTTP — port 8765 also works, but real-world networks sometimes filter unusual ports)
   (and 22 for SSH).
2. 👤 **SSH in and fetch the repo:**
   ```bash
   ssh root@<instance-ip>
   git clone https://github.com/jksim26/Trace.git && cd Trace
   # (while the repo is private, use a personal access token or scp the repo up)
   ```
3. 👤 **Create `Trace/.env` on the instance** (never commit this):
   ```bash
   echo "DASHSCOPE_API_KEY=sk-..." > Trace/.env
   ```
4. **Deploy:**
   ```bash
   sudo bash deploy/deploy_alibaba.sh
   ```
   The script installs a venv + dependencies, **runs the offline test suite as a
   deployment gate**, then installs and starts a `trace-bubble` systemd service
   on `0.0.0.0:80`.
5. **Verify:** open `http://<instance-ip>` — the bubble should render, and
   the chat box should answer (a real `recall_decisions` → Qwen call). If /ask
   fails, check the key: `journalctl -u trace-bubble -f`.
6. 👤 **Paste the URL** into the Devpost submission as the testing-access link,
   and link the proof files above.

## Operations

```bash
systemctl status trace-bubble      # health
journalctl -u trace-bubble -f      # logs
systemctl restart trace-bubble     # after a git pull
```

Keep the instance running through **31 July** (end of the judging period) — the
rules require free access for testing until then.
