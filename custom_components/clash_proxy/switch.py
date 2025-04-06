"""Clash代理开关实体"""
import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from .const import DATA_CLIENT, DOMAIN, ICON_PROXY

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置Clash开关实体"""
    client = hass.data[DOMAIN][config_entry.entry_id][DATA_CLIENT]
    
    async_add_entities([ClashProxySwitch(client)])


class ClashProxySwitch(SwitchEntity):
    """代表Clash代理开关的实体"""

    def __init__(self, client):
        """初始化开关"""
        self._client = client
        self._attr_name = "Clash代理"
        self._attr_unique_id = f"{DOMAIN}_proxy_switch"
        self._attr_icon = ICON_PROXY
        self._attr_is_on = client.running

    @property
    def is_on(self) -> bool:
        """返回开关状态"""
        return self._client.running

    async def async_turn_on(self, **kwargs: Any) -> None:
        """打开代理"""
        await self.hass.async_add_executor_job(self._client.start)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """关闭代理"""
        await self.hass.async_add_executor_job(self._client.stop)
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """返回额外的状态属性"""
        return {
            "subscription_url": self._client.subscription_url,
            "proxy_mode": self._client.proxy_mode,
            "allow_lan": self._client.allow_lan,
            "log_level": self._client.log_level,
            "auto_update": self._client.auto_update,
            "update_interval": self._client.update_interval,
        } 