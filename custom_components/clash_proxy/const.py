"""Clash代理集成的常量"""

DOMAIN = "clash_proxy"

CONF_SUBSCRIPTION_URL = "subscription_url"
CONF_PROXY_MODE = "proxy_mode"
CONF_ALLOW_LAN = "allow_lan"
CONF_LOG_LEVEL = "log_level"
CONF_AUTO_UPDATE = "auto_update"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_AUTO_SELECT_SUPER = "auto_select_super"

DATA_CLIENT = "client"
DATA_CONFIG = "config"
DATA_UPDATED = "updated"

SERVICE_UPDATE_CONFIG = "update_config"
SERVICE_TOGGLE_PROXY = "toggle_proxy"

# 默认端口
DEFAULT_HTTP_PORT = 7890
DEFAULT_SOCKS_PORT = 7891
DEFAULT_API_PORT = 9090

# 实体ID前缀
ENTITY_ID_FORMAT = DOMAIN + ".{}"

# 图标
ICON_PROXY = "mdi:cloud-sync"
ICON_TRAFFIC = "mdi:swap-vertical"
ICON_LATENCY = "mdi:timer-outline"

# 单位
UNIT_BYTES_PER_SEC = "B/s"
UNIT_MILLISECONDS = "ms"

# 传感器类型
SENSOR_TYPE_UPLOAD = "upload"
SENSOR_TYPE_DOWNLOAD = "download"
SENSOR_TYPE_LATENCY = "latency" 