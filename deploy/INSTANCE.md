# Live Alibaba Cloud ECS instance — the deployed Trace demo

The single source of truth for **where the live demo runs**, so we never have to
go re-discover it. (Public IP is not a secret — it's the judges' testing-access
link on Devpost. The API key and SSH password live only on the box, never here.)

## The instance

| | |
|---|---|
| **Live URL** | **http://47.245.82.206**  (port 80, plain HTTP — no `:8765`, no `https`) |
| **Public IP** | `47.245.82.206` |
| **Host name** | `iZt4n3a409jb8sw4nsk04zZ` |
| **Region / zone** | Singapore — `ap-southeast-1`, Zone B (same region as the DashScope endpoint) |
| **OS** | Ubuntu 22.04 |
| **Spec** | smallest tier, ~2 vCPU / 4 GiB (e-series, e.g. `ecs.e-c1m2.large`) — approximate |
| **SSH** | `ssh root@47.245.82.206` (password set during setup — not stored here) |
| **App** | systemd service `trace-bubble`, `bubble.py` bound to `0.0.0.0:80` |
| **Secret on box** | `Trace/.env` → `DASHSCOPE_API_KEY=...` (never committed) |
| **Repo path on box** | `~/Trace` |

## Keep it alive
The rules require free testing access through **31 July 2026** — do **not** stop or
release the instance before then.

## Deploy / update to the latest `main`
```bash
cd ~/Trace
git fetch origin
git checkout main
git reset --hard origin/main      # mirror remote main exactly; .env is untracked, so it survives
sudo systemctl restart trace-bubble
```
No `pip install` needed for a UI change (the `mcp` dep is only for `mcp_server.py`).

## Health / debug
```bash
systemctl status trace-bubble         # active (running)?
journalctl -u trace-bubble -n 50      # recent logs
curl -s http://100.100.100.200/latest/meta-data/eipv4   # confirm the public IP from the box
```

## Get the public IP if this doc ever goes stale
Alibaba Cloud console → ECS → the instance → **Public IP**, or run the `curl`
metadata command above on the box.
