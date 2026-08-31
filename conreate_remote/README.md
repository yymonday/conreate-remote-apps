# Conreate Remote Home Assistant App

Install the repository in Home Assistant, set the HTTPS Control Plane domain and a one-time activation code, then start the App. The Agent identity and issued device token persist in the App configuration directory.

On every startup with an enrolled device, the App log clearly prints `你的 Home Assistant 远程访问网址 / Remote access URL: ...` and the **HA 反向代理信任地址 / HA trusted proxy address**. A sanitized `/config/status.json` also records the current phase, Device ID, remote URL, trusted proxy address, message, and update time; it never contains the device token, FRP credential, activation code, or private identity key. If HA returns HTTP 400, the status changes to `configuration_required` and points the administrator to Home Assistant's UI-based reverse-proxy settings with the exact address to copy, instead of asking the customer to edit YAML.

The App defaults to Home Assistant at `homeassistant:8123`. For installations using another internal port, configure `local_addr` and `local_port` in the App options; the port is validated before the Agent starts.

This App does not modify Home Assistant users or authentication. Remote visitors still sign in to Home Assistant normally.

For recovery, stop the App, clear its lost/invalid Agent state as directed by support, then enter both the administrator-issued recovery code and original Device ID. Recovery replaces the device identity/token while retaining its assigned remote hostname. Do not enter an activation code at the same time.

The App image contains the exact version-matched Agent Core package and frpc binary. The Agent image is a private build input; only this customer-facing HA App image is published publicly. Keeping Agent Core as the single implementation prevents the HA wrapper from becoming a second implementation.

For a local Linux/amd64 packaging check, run `python scripts/ha_demo_check.py --build` from the repository root. A real HA OS installation still requires published `amd64` and `aarch64` images in a registry accessible to the Supervisor.
