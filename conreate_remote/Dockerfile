ARG BUILD_ARCH=amd64
ARG AGENT_IMAGE=ghcr.io/yymonday/conreate-remote-agent:0.1.1
FROM ${AGENT_IMAGE} AS agent_core
FROM ghcr.io/home-assistant/${BUILD_ARCH}-base:3.19
ARG BUILD_ARCH
ARG BUILD_VERSION=0.1.1
LABEL \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="app" \
    io.hass.arch="${BUILD_ARCH}" \
    org.opencontainers.image.source="https://github.com/yymonday/conreate-cloud"
RUN apk add --no-cache python3 py3-pip
COPY agent-requirements.txt /tmp/requirements.txt
RUN pip3 install --break-system-packages --no-cache-dir -r /tmp/requirements.txt
COPY --from=agent_core /usr/local/bin/frpc /usr/local/bin/frpc
COPY --from=agent_core /usr/share/licenses/frp/LICENSE /usr/share/licenses/frp/LICENSE
COPY --from=agent_core /app/conreate_agent /app/conreate_agent
COPY run.sh /run.sh
RUN chmod +x /run.sh
WORKDIR /app
CMD ["/run.sh"]
