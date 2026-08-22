# Conreate Remote Home Assistant App

Install the repository in Home Assistant, set the HTTPS Control Plane domain and a one-time activation code, then start the App. The Agent identity and issued device token persist in the App configuration directory.

On a successful connection, the App log prints the assigned remote URL. A sanitized `/config/status.json` also records the current phase, Device ID, remote URL, message, and update time; it never contains the device token, FRP credential, activation code, or private identity key.

The App defaults to Home Assistant at `homeassistant:8123`. For installations using another internal port, configure `local_addr` and `local_port` in the App options; the port is validated before the Agent starts.

This App does not modify Home Assistant users or authentication. Remote visitors still sign in to Home Assistant normally.

For recovery, stop the App, clear its lost/invalid Agent state as directed by support, then enter both the administrator-issued recovery code and original Device ID. Recovery replaces the device identity/token while retaining its assigned remote hostname. Do not enter an activation code at the same time.

The App image copies the exact Agent Core package and frpc binary from the published, version-matched `conreate-remote-agent` image. Publish the multi-architecture Agent image before building the App release; this keeps the HA wrapper from becoming a second implementation.

For a local Linux/amd64 packaging check, run `python scripts/ha_demo_check.py --build` from the repository root. A real HA OS installation still requires published `amd64` and `aarch64` images in a registry accessible to the Supervisor.
