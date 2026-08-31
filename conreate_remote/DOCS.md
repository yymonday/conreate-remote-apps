# Conreate Remote

Conreate Remote connects this Home Assistant installation to a self-hosted Conreate Cloud server. Device activation is independent of Home Assistant user authentication; anyone opening the assigned remote URL must still sign in to Home Assistant normally.

## Before installation

Ask the Conreate Cloud administrator for:

- the HTTPS Control Plane URL, such as `https://api.example.com`;
- a one-time activation code;
- confirmation that the Agent and App image version matches this release.

## First activation

1. Enter the Control Plane URL and one-time activation code in the App configuration.
2. Keep `Home Assistant URL` at `http://homeassistant:8123` on HA OS unless your installation requires another reachable address.
3. If Home Assistant listens on a non-default port, set `local_addr` and `local_port` to the address reachable from the App, such as `homeassistant` and `7277`.
4. Save and start the App.
5. Open the App log. After activation it shows the assigned remote HTTPS URL.
6. Open that URL from an external network and sign in with an existing Home Assistant user.

To find the address again later, open the App's **Log** tab and search for `你的 Home Assistant 远程访问网址` or `Remote access URL`. The same address is also saved in the App's sanitized `status.json` as `remote_url`; from inside the App it is `/config/status.json`, and on HA OS it is under the App's `/addon_configs/conreate_remote/` directory when that directory is exposed by a file-management add-on. The status file also reports `trusted_proxy_address`, the source address the App uses to reach Home Assistant. Add it with `/32` to Home Assistant's trusted proxy list when the remote page returns HTTP 400. The Conreate Cloud Admin Console labels both values explicitly and provides copy actions.

The App stores its generated device identity and issued credentials in its persistent configuration directory. Do not copy or publish those files.

## Recovery

If the device is shown as revoked or its persistent state is lost, stop the App and obtain a recovery code plus the original Device ID from the Conreate Cloud administrator. Creating the recovery code immediately revokes the old connection. Enter both recovery values and restart the App; an existing one-time activation value is ignored when local state already exists. Recovery keeps the assigned Device ID and hostname while replacing the device token. After the App reconnects, clear both recovery fields so they are not retained in the App options.

## Troubleshooting

- `invalid_activation_code`: request a new unused activation code.
- `subscription_inactive` or `device_limit_reached`: ask the administrator to check the project subscription.
- repeated connection retries: verify DNS, outbound HTTPS, the FRP server domain/port, and server availability.
- `token in NewWorkConn doesn't match token from configuration`: use an App/container diagnostic path, not the HA host shell; do not share `frpc.toml`. The release keeps native `NewWorkConns` disabled and relies on the Control Plane device-authorizer plugin for per-device work-connection authorization.
- the assigned URL returns HTTP 400: the tunnel has reached Home Assistant, but HA has not accepted the reverse proxy. In Home Assistant 2026.8 or later, open **Settings → System → Network → HTTP Server → Reverse proxy**, enable X-Forwarded-For trust, and add the App's clearly labeled **HA trusted proxy address** with `/32`. The same address is shown in the App log and `status.json`, while the Admin Console shows and copies it on the device card. The customer does not need to edit YAML.
- the remote page opens but login fails: use a valid Home Assistant user; Conreate activation does not create HA users.

The sanitized status file at `/config/status.json` may be shared with support. Never share device state, private keys, generated FRP configuration, activation codes, or recovery codes.
