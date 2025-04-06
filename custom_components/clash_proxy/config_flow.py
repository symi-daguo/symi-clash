"""配置流程处理"""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_SUBSCRIPTION_URL,
    CONF_PROXY_MODE,
    CONF_ALLOW_LAN,
    CONF_LOG_LEVEL,
    CONF_AUTO_UPDATE,
    CONF_UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class ClashProxyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理Clash代理配置流程"""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None) -> FlowResult:
        """处理用户输入的配置"""
        errors = {}

        if user_input is not None:
            subscription_url = user_input[CONF_SUBSCRIPTION_URL]
            
            # 验证订阅URL是否有效
            # 这里可以添加异步验证逻辑
            
            await self.async_set_unique_id(subscription_url)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Clash Proxy ({subscription_url[:20]}...)",
                data=user_input,
            )

        # 如果没有用户输入或有错误，显示表单
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SUBSCRIPTION_URL): str,
                    vol.Optional(CONF_PROXY_MODE, default="rule"): vol.In(
                        ["rule", "global", "direct"]
                    ),
                    vol.Optional(CONF_ALLOW_LAN, default=True): bool,
                    vol.Optional(CONF_LOG_LEVEL, default="info"): vol.In(
                        ["info", "debug", "warning", "error", "silent"]
                    ),
                    vol.Optional(CONF_AUTO_UPDATE, default=True): bool,
                    vol.Optional(CONF_UPDATE_INTERVAL, default=12): vol.All(
                        vol.Coerce(int), vol.Range(min=1, max=24)
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """获取选项流程处理器"""
        return ClashProxyOptionsFlow(config_entry)


class ClashProxyOptionsFlow(config_entries.OptionsFlow):
    """Clash选项流程处理"""

    def __init__(self, config_entry):
        """初始化选项流程"""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """管理选项"""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_PROXY_MODE,
                        default=self.config_entry.options.get(
                            CONF_PROXY_MODE, 
                            self.config_entry.data.get(CONF_PROXY_MODE, "rule")
                        ),
                    ): vol.In(["rule", "global", "direct"]),
                    vol.Optional(
                        CONF_ALLOW_LAN,
                        default=self.config_entry.options.get(
                            CONF_ALLOW_LAN, 
                            self.config_entry.data.get(CONF_ALLOW_LAN, True)
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_LOG_LEVEL,
                        default=self.config_entry.options.get(
                            CONF_LOG_LEVEL, 
                            self.config_entry.data.get(CONF_LOG_LEVEL, "info")
                        ),
                    ): vol.In(["info", "debug", "warning", "error", "silent"]),
                    vol.Optional(
                        CONF_AUTO_UPDATE,
                        default=self.config_entry.options.get(
                            CONF_AUTO_UPDATE, 
                            self.config_entry.data.get(CONF_AUTO_UPDATE, True)
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL, 
                            self.config_entry.data.get(CONF_UPDATE_INTERVAL, 12)
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
                }
            ),
        ) 