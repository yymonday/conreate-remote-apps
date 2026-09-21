# 0.2.0-rc.2

- Show “服务已到期” when Conreate Cloud reports that the device service term has expired.
- Stop the remote tunnel on service expiry while retaining the device identity; reconnect after an administrator extends service or grants temporary access.
- Fix bundled Agent source permissions for restricted runtime environments.
- Existing devices with no configured service expiry retain their current access. Home Assistant user authentication is unchanged.

Requires the Conreate Cloud RC2 server. Self-service payment is not enabled in this release.
