"""配置流程处理"""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_SUBSCRIPTION_URL,
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

            # 使用默认设置，简化配置
            user_input.update({
                "proxy_mode": "rule",
                "allow_lan": True,
                "log_level": "info",
                "auto_update": True,
                "update_interval": 12,
                "auto_select_super": True,  # 新增: 自动选择super代理组
            })

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

        # 简化选项配置
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "auto_select_super",
                        default=self.config_entry.options.get(
                            "auto_select_super",
                            self.config_entry.data.get("auto_select_super", True)
                        ),
                    ): bool,
                }
            ),
        ) 