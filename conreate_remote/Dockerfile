ARG AGENT_IMAGE=ccr.ccs.tencentyun.com/conreateknx/conreate-remote-agent:0.1.9
FROM ${AGENT_IMAGE} AS agent_core

FROM ghcr.io/home-assistant/base-python:3.14-alpine3.24
ARG BUILD_ARCH
ARG BUILD_VERSION=0.1.9
LABEL \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="app" \
    io.hass.arch="${BUILD_ARCH}" \
    org.opencontainers.image.source="https://github.com/yymonday/conreate-remote-apps"
# tempio is optional tooling from the HA base image. This App does not invoke
# it; remove the stale Go binary so its bundled vulnerable dependencies are not
# exposed in the customer-facing runtime.
RUN apk upgrade --no-cache && rm -f /usr/bin/tempio
COPY agent-requirements.txt /tmp/requirements.txt
RUN pip3 install --break-system-packages --no-cache-dir --timeout 300 --retries 10 -r /tmp/requirements.txt
COPY --from=agent_core /usr/local/bin/frpc /usr/local/bin/frpc
COPY --from=agent_core /usr/share/licenses/frp/LICENSE /usr/share/licenses/frp/LICENSE
COPY --from=agent_core /app/conreate_agent /app/conreate_agent
COPY run.sh /run.sh
RUN chmod +x /run.sh
WORKDIR /app
CMD ["/run.sh"]
