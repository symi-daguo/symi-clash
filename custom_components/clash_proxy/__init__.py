"""Clash代理集成组件"""
import logging
import os
import tempfile
import time
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_BINARY_SENSORS,
    CONF_NAME,
    CONF_SENSORS,
    CONF_SWITCHES,
    Platform,
)
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_AUTO_UPDATE,
    CONF_SUBSCRIPTION_URL,
    CONF_PROXY_MODE,
    CONF_ALLOW_LAN,
    CONF_LOG_LEVEL,
    CONF_UPDATE_INTERVAL,
    DATA_CLIENT,
    DATA_CONFIG,
    DATA_UPDATED,
    DOMAIN,
    SERVICE_UPDATE_CONFIG,
    SERVICE_TOGGLE_PROXY
)
from .clash_client import ClashClient

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_SUBSCRIPTION_URL): cv.string,
                vol.Optional(CONF_PROXY_MODE, default="rule"): cv.string,
                vol.Optional(CONF_ALLOW_LAN, default=True): cv.boolean,
                vol.Optional(CONF_LOG_LEVEL, default="info"): cv.string,
                vol.Optional(CONF_AUTO_UPDATE, default=True): cv.boolean,
                vol.Optional(CONF_UPDATE_INTERVAL, default=12): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=24)
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = [Platform.SWITCH]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """设置Clash集成"""
    if DOMAIN not in config:
        return True

    hass.data.setdefault(DOMAIN, {})
    conf = config[DOMAIN]
    hass.data[DOMAIN][DATA_CONFIG] = conf
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """从配置条目设置Clash集成"""
    hass.data.setdefault(DOMAIN, {})
    
    subscription_url = entry.data.get(CONF_SUBSCRIPTION_URL)
    proxy_mode = entry.data.get(CONF_PROXY_MODE, "rule")
    allow_lan = entry.data.get(CONF_ALLOW_LAN, True)
    log_level = entry.data.get(CONF_LOG_LEVEL, "info")
    auto_update = entry.data.get(CONF_AUTO_UPDATE, True)
    update_interval = entry.data.get(CONF_UPDATE_INTERVAL, 12)
    
    client = ClashClient(
        subscription_url=subscription_url,
        proxy_mode=proxy_mode,
        allow_lan=allow_lan,
        log_level=log_level,
        auto_update=auto_update,
        update_interval=update_interval,
    )
    
    await hass.async_add_executor_job(client.start)
    
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_UPDATED: time.time(),
    }

    # 注册服务
    async def handle_update_config(call: ServiceCall) -> None:
        """处理更新配置服务调用"""
        client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
        subscription_url = call.data.get(CONF_SUBSCRIPTION_URL, client.subscription_url)
        await hass.async_add_executor_job(
            client.update_config, subscription_url
        )
        hass.data[DOMAIN][entry.entry_id][DATA_UPDATED] = time.time()

    async def handle_toggle_proxy(call: ServiceCall) -> None:
        """处理切换代理服务调用"""
        client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
        enabled = call.data.get("enabled")
        if enabled is not None:
            await hass.async_add_executor_job(
                client.set_enabled, enabled
            )

    hass.services.async_register(
        DOMAIN, SERVICE_UPDATE_CONFIG, handle_update_config
    )
    
    hass.services.async_register(
        DOMAIN, SERVICE_TOGGLE_PROXY, handle_toggle_proxy
    )
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载Clash集成条目"""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
        await hass.async_add_executor_job(client.stop)
        hass.data[DOMAIN].pop(entry.entry_id)
        
    return unload_ok 