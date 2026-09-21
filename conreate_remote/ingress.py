#!/usr/bin/env python3
"""Small read-only Home Assistant Ingress UI for sanitized Agent status."""
import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("conreate-remote-ingress")
STATUS_PATH = Path(os.environ.get("CONREATE_STATUS_PATH", "/config/status.json"))
MAX_STATUS_BYTES = 64 * 1024
PUBLIC_STRING_LIMITS = {
    "phase": 40,
    "device_id": 80,
    "message": 1000,
    "updated_at": 80,
    "route_change_status": 20,
    "route_change_error": 500,
}


def load_public_status(path: Optional[Path] = None) -> dict:
    """Return an explicit allowlist; never expose Agent state or credentials."""
    path = path or STATUS_PATH
    try:
        if path.stat().st_size > MAX_STATUS_BYTES:
            raise ValueError("status file is unexpectedly large")
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("status payload is not an object")
    except (OSError, ValueError, json.JSONDecodeError):
        return {"available": False, "phase": "starting",
                "message": "Conreate Remote status is not available yet"}

    result = {"available": True}
    for key, limit in PUBLIC_STRING_LIMITS.items():
        value = raw.get(key)
        result[key] = value[:limit] if isinstance(value, str) else None
    for key in ("assignment_revision", "applied_assignment_revision"):
        value = raw.get(key)
        result[key] = value if isinstance(value, int) and value > 0 else None

    remote_url = raw.get("remote_url")
    if isinstance(remote_url, str):
        parsed = urlsplit(remote_url)
        if parsed.scheme in {"https", "http"} and parsed.hostname and not parsed.username:
            result["remote_url"] = remote_url[:2048]
        else:
            result["remote_url"] = None
    else:
        result["remote_url"] = None

    proxy_address = raw.get("trusted_proxy_address")
    try:
        result["trusted_proxy_address"] = str(ip_address(proxy_address)) if proxy_address else None
    except ValueError:
        result["trusted_proxy_address"] = None
    return result


APP_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="color-scheme" content="light dark">
  <title>Conreate Remote</title>
  <style>
    :root{color-scheme:light;--bg:#f3f6f4;--card:#fff;--ink:#17231d;--muted:#6f7e76;--line:#dfe7e2;--brand:#176044;--brand-soft:#e4f2ea;--amber:#8d642a;--amber-bg:#fbf4e8;--red:#984942;--red-bg:#fbefed;--shadow:0 16px 44px rgba(25,51,38,.10)}
    *{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(circle at 100% 0,#dcefe4 0,transparent 32%),var(--bg);color:var(--ink);font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}.shell{width:min(760px,100%);margin:auto;padding:28px 18px 44px}.top{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:24px}.brand{display:flex;align-items:center;gap:12px}.mark{display:grid;place-items:center;width:42px;height:42px;border-radius:13px;background:var(--brand);color:#fff;font-weight:900;letter-spacing:-.06em;box-shadow:0 8px 22px rgba(23,96,68,.22)}h1{margin:0;font-size:21px;letter-spacing:-.03em}.brand small{display:block;color:var(--muted);font-size:11px}.badge{padding:6px 10px;border-radius:999px;background:#e7efea;color:#496157;font-size:11px;font-weight:800}.badge.ok{background:var(--brand-soft);color:var(--brand)}.badge.warn{background:var(--amber-bg);color:var(--amber)}.badge.bad{background:var(--red-bg);color:var(--red)}.card{padding:22px;border:1px solid var(--line);border-radius:18px;background:var(--card);box-shadow:var(--shadow)}.eyebrow{margin:0 0 7px;color:#839088;font-size:10px;font-weight:850;letter-spacing:.14em}.url{display:block;margin:0;color:var(--brand);font-size:clamp(17px,4vw,24px);font-weight:850;letter-spacing:-.025em;overflow-wrap:anywhere;text-decoration:none}.url.disabled{color:#8b9790;pointer-events:none}.actions{display:flex;gap:10px;margin-top:18px}.actions button,.actions a{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:0 16px;border:1px solid #cfdad4;border-radius:10px;background:#fff;color:#3e5549;font:inherit;font-weight:750;text-decoration:none;cursor:pointer}.actions .primary{border-color:var(--brand);background:var(--brand);color:#fff}.actions [aria-disabled=true]{opacity:.45;pointer-events:none}.route{display:none;margin-top:16px;padding:12px 14px;border:1px solid #ead8b9;border-radius:11px;background:var(--amber-bg);color:#765523}.route.failed{border-color:#eccdca;background:var(--red-bg);color:var(--red)}.route strong,.route span{display:block}.route span{margin-top:3px;font-size:12px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}.metric{min-width:0;padding:15px;border:1px solid var(--line);border-radius:13px;background:rgba(255,255,255,.82)}.metric span,.metric strong{display:block}.metric span{color:var(--muted);font-size:10px;font-weight:750}.metric strong{margin-top:5px;font-size:13px;overflow-wrap:anywhere}.guide{display:none;margin-top:14px;padding:16px 18px;border:1px solid #ead8b9;border-radius:13px;background:var(--amber-bg)}.guide h2{margin:0 0 6px;font-size:14px}.guide p{margin:0;color:#765f3d;font-size:12px}.guide code{display:block;margin-top:9px;padding:8px 10px;border-radius:7px;background:rgba(255,255,255,.72);font-size:12px;overflow-wrap:anywhere}.foot{margin:17px 3px 0;color:#849189;font-size:11px}.foot strong{color:#5e6e65}.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(16px);padding:10px 14px;border-radius:9px;background:#183326;color:#fff;font-size:12px;opacity:0;pointer-events:none;transition:.2s}.toast.show{transform:translateX(-50%) translateY(0);opacity:1}@media(max-width:560px){.shell{padding:20px 13px 34px}.top{align-items:flex-start}.card{padding:18px}.actions{display:grid;grid-template-columns:1fr 1fr}.grid{grid-template-columns:1fr}.metric{display:flex;align-items:center;justify-content:space-between;gap:12px}.metric strong{margin:0;text-align:right}}
    @media(prefers-color-scheme:dark){:root{color-scheme:dark;--bg:#101713;--card:#17211c;--ink:#eef5f0;--muted:#93a198;--line:#2d3a33;--brand:#70d4a4;--brand-soft:#203e30;--amber:#e1b66f;--amber-bg:#342b1e;--red:#efaaa3;--red-bg:#3a2422;--shadow:none}body{background:radial-gradient(circle at 100% 0,#1b392a 0,transparent 34%),var(--bg)}.actions button,.actions a{border-color:#405047;background:#1b2821;color:#dbe8df}.actions .primary{border-color:#31855f;background:#26714f;color:#fff}.metric{background:#17211c}.guide code{background:rgba(0,0,0,.16)}}
  </style>
</head>
<body>
  <main class="shell">
    <header class="top"><div class="brand"><span class="mark">CR</span><div><h1>Conreate Remote</h1><small>Home Assistant 远程访问</small></div></div><span id="phase" class="badge warn">正在读取</span></header>
    <section class="card"><p class="eyebrow">当前 HA 远程访问网址</p><a id="url" class="url disabled" href="#" target="_blank" rel="noreferrer">等待设备连接…</a><div class="actions"><button id="copy" class="primary" disabled>复制网址</button><a id="open" href="#" target="_blank" rel="noreferrer" aria-disabled="true">打开 HA ↗</a></div><div id="route" class="route"><strong id="route-title"></strong><span id="route-detail"></span></div></section>
    <section class="grid"><article class="metric"><span>隧道状态</span><strong id="tunnel">等待上报</strong></article><article class="metric"><span>网址版本</span><strong id="revision">—</strong></article><article class="metric"><span>最近更新</span><strong id="updated">—</strong></article></section>
    <section id="guide" class="guide"><h2>已到达 HA，但需要配置反向代理</h2><p>打开“设置 → 系统 → 网络 → HTTP Server → Reverse proxy”，添加下面的 App 信任地址。无需修改 YAML。</p><code id="proxy">等待 App 上报</code></section>
    <p class="foot"><strong>安全说明：</strong>此页由 Home Assistant Ingress 保护，只读取脱敏状态；不会显示设备令牌、FRP 凭据、激活码或 HA 用户密码。页面每 5 秒自动刷新。</p>
  </main><div id="toast" class="toast" role="status"></div>
  <script>
    const $=id=>document.getElementById(id);let currentUrl="";
    const phaseLabels={starting:"正在启动",activating:"正在激活",recovering:"正在恢复",tunnel_starting:"隧道切换中",connected:"连接正常",configuration_required:"HA 待配置",retrying:"正在重连",service_expired:"服务已到期",revoked:"设备已撤销",configuration_error:"配置错误"};
    function cidr(value){return value?value+(value.includes(":")?"/128":"/32"):"等待 App 上报"}
    function timeText(value){if(!value)return "—";const date=new Date(value);return Number.isNaN(date.getTime())?"—":new Intl.DateTimeFormat("zh-CN",{month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit"}).format(date)}
    function toast(text){const item=$("toast");item.textContent=text;item.classList.add("show");setTimeout(()=>item.classList.remove("show"),1800)}
    function paint(s){
      const phase=s.phase||"starting",badge=$("phase");badge.textContent=phaseLabels[phase]||phase;badge.className="badge "+(["connected"].includes(phase)?"ok":["revoked","configuration_error","service_expired"].includes(phase)?"bad":"warn");
      currentUrl=s.remote_url||"";const url=$("url"),open=$("open"),copy=$("copy");url.textContent=currentUrl||"等待设备连接…";url.href=currentUrl||"#";url.classList.toggle("disabled",!currentUrl);open.href=currentUrl||"#";open.setAttribute("aria-disabled",String(!currentUrl));copy.disabled=!currentUrl;
      $("tunnel").textContent=phaseLabels[phase]||phase;const desired=s.assignment_revision,applied=s.applied_assignment_revision;$("revision").textContent=desired?(desired===applied?`v${applied} 已生效`:`v${applied||"—"} → v${desired}`):"—";$("updated").textContent=timeText(s.updated_at);
      const route=$("route"),routeState=s.route_change_status;route.style.display=routeState==="pending"||routeState==="failed"?"block":"none";route.className="route "+(routeState==="failed"?"failed":"");$("route-title").textContent=routeState==="failed"?"上次网址切换失败":"正在确认新网址";$("route-detail").textContent=routeState==="failed"?(s.route_change_error||"设备已返回当前可用网址。"):`新版本 v${desired||"—"} 已下发；探测成功后自动生效。`;
      const needsProxy=phase==="configuration_required";$("guide").style.display=needsProxy?"block":"none";$("proxy").textContent=cidr(s.trusted_proxy_address);
    }
    async function refresh(){try{const response=await fetch("./api/status",{cache:"no-store"});if(!response.ok)throw new Error(`HTTP ${response.status}`);paint(await response.json())}catch(error){paint({phase:"retrying"});$("route").style.display="block";$("route-title").textContent="状态暂不可用";$("route-detail").textContent=String(error)}}
    $("copy").addEventListener("click",async()=>{if(!currentUrl)return;try{await navigator.clipboard.writeText(currentUrl);toast("网址已复制")}catch{const input=document.createElement("textarea");input.value=currentUrl;document.body.appendChild(input);input.select();document.execCommand("copy");input.remove();toast("网址已复制")}});
    refresh();setInterval(refresh,5000);
  </script>
</body></html>'''.encode("utf-8")


class IngressHandler(BaseHTTPRequestHandler):
    server_version = "ConreateRemoteIngress/1"
    sys_version = ""
    protocol_version = "HTTP/1.1"

    def version_string(self) -> str:
        return self.server_version

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
                         "connect-src 'self'; frame-ancestors 'self'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        path = urlsplit(self.path).path.rstrip("/")
        if path == "/api/status":
            body = json.dumps(load_public_status(), ensure_ascii=False).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
        elif path == "/healthz":
            self._send(200, b'{"status":"ok"}', "application/json; charset=utf-8")
        else:
            self._send(200, APP_HTML, "text/html; charset=utf-8")

    def log_message(self, format_string: str, *args) -> None:
        log.debug(format_string, *args)


def main() -> None:
    port = int(os.environ.get("CONREATE_INGRESS_PORT", "8099"))
    server = ThreadingHTTPServer(("0.0.0.0", port), IngressHandler)
    log.info("Conreate Remote Ingress status page listening on port %s", port)
    server.serve_forever()


if __name__ == "__main__":
    main()
