#!/usr/bin/with-contenv bashio
export CONREATE_CONTROL_PLANE_URL="$(bashio::config 'control_plane_url')"
export CONREATE_ACTIVATION_CODE="$(bashio::config 'activation_code')"
export CONREATE_RECOVERY_CODE="$(bashio::config 'recovery_code')"
export CONREATE_RECOVER_DEVICE_ID="$(bashio::config 'recover_device_id')"
export CONREATE_DEVICE_NAME="$(bashio::config 'device_name')"
export CONREATE_LOCAL_ADDR="$(bashio::config 'local_addr')"
export CONREATE_LOCAL_PORT="$(bashio::config 'local_port')"
export CONREATE_STATE_DIR="/config"

if [[ "${CONREATE_CONTROL_PLANE_URL}" != https://* ]]; then
    bashio::log.fatal "Control Plane 地址必须使用 https:// 域名。"
    exit 1
fi

if ! [[ "${CONREATE_LOCAL_PORT}" =~ ^[0-9]+$ ]] || (( CONREATE_LOCAL_PORT < 1 || CONREATE_LOCAL_PORT > 65535 )); then
    bashio::log.fatal "本地 HA 端口必须是 1-65535。"
    exit 1
fi

if [[ -z "${CONREATE_LOCAL_ADDR}" || "${CONREATE_LOCAL_ADDR}" == "0.0.0.0" || "${CONREATE_LOCAL_ADDR}" == "127.0.0.1" ]]; then
    bashio::log.fatal "本地 HA 地址不能为空，且不能使用 0.0.0.0 或 127.0.0.1。"
    exit 1
fi

if [[ -n "${CONREATE_RECOVERY_CODE}" || -n "${CONREATE_RECOVER_DEVICE_ID}" ]]; then
    if [[ -z "${CONREATE_RECOVERY_CODE}" || -z "${CONREATE_RECOVER_DEVICE_ID}" ]]; then
        bashio::log.fatal "设备恢复必须同时填写恢复码和原 Device ID，不能只填写其中一项。"
        exit 1
    fi
fi

if [[ ! -f /config/agent-state.json ]]; then
    if [[ -n "${CONREATE_ACTIVATION_CODE}" && ( -n "${CONREATE_RECOVERY_CODE}" || -n "${CONREATE_RECOVER_DEVICE_ID}" ) ]]; then
        bashio::log.fatal "激活码不能与恢复码同时填写。"
        exit 1
    fi
    if [[ -z "${CONREATE_ACTIVATION_CODE}" && -z "${CONREATE_RECOVERY_CODE}" ]]; then
        bashio::log.fatal "首次启动必须填写激活码；设备恢复必须同时填写恢复码和原 Device ID。"
        exit 1
    fi
fi

bashio::log.info "正在启动 Conreate Remote；设备身份保存在 App 私有配置目录。"
exec python3 -m conreate_agent.main
