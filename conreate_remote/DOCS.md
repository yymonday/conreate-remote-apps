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
3. Save and start the App.
4. Open the App log. After activation it shows the assigned remote HTTPS URL.
5. Open that URL from an external network and sign in with an existing Home Assistant user.

The App stores its generated device identity and issued credentials in its persistent configuration directory. Do not copy or publish those files.

## Recovery

If the persistent device state is lost, stop the App and obtain a recovery code plus the original Device ID from the Conreate Cloud administrator. Enter both recovery values and leave the activation code empty. Recovery keeps the assigned hostname while replacing the device identity and token.

## Troubleshooting

- `invalid_activation_code`: request a new unused activation code.
- `subscription_inactive` or `device_limit_reached`: ask the administrator to check the project subscription.
- repeated connection retries: verify DNS, outbound HTTPS, the FRP server domain/port, and server availability.
- the remote page opens but login fails: use a valid Home Assistant user; Conreate activation does not create HA users.

The sanitized status file at `/config/status.json` may be shared with support. Never share device state, private keys, generated FRP configuration, activation codes, or recovery codes.
