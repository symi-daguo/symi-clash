# Clash Proxy for Home Assistant

这是一个为 Home Assistant 设计的 Clash 代理服务集成，只需提供订阅地址，即可在 Home Assistant 中使用代理服务。符合2025年Home Assistant集成标准。

## 功能特点

- **超级简单**：只需输入订阅地址，无需复杂配置
- **自动连接**：自动查找并连接到Super代理组
- **完全集成**：作为 Home Assistant 集成运行，通过HACS安装
- **支持多种代理协议**：Shadowsocks、V2Ray、Trojan 等
- **自动更新**：定时自动更新订阅配置
- **便捷控制**：通过开关实体一键启用/禁用代理

## 安装方法

### 使用HACS安装（推荐）

1. 确保已安装 [HACS](https://hacs.xyz/)
2. 在HACS中添加自定义仓库：
   - 类型: 集成
   - URL: `https://github.com/symi-daguo/symi-clash`
3. 在HACS中搜索并安装 "Clash Proxy"
4. 重启 Home Assistant
5. 在集成页面中，点击右下角的"+ 添加集成"按钮
6. 搜索 "Clash Proxy"（如果找不到，请尝试搜索"clash"或"proxy"）
7. 只需输入订阅地址，其他一切自动配置

### 手动安装

1. 下载此仓库
2. 将 `custom_components/clash_proxy` 目录复制到您的 Home Assistant 配置目录的 `custom_components` 文件夹中
3. 重启 Home Assistant
4. 在集成页面中，点击右下角的"+ 添加集成"按钮
5. 搜索 "Clash Proxy"（如果找不到，请尝试搜索"clash"或"proxy"）
6. 只需输入订阅地址，其他一切自动配置

## 简化使用流程

本集成专为简化使用而设计：

1. **仅需输入订阅地址**：其他所有配置都使用合理的默认值，无需手动设置
2. **自动连接Super代理组**：会自动识别订阅中的Super代理组并自动连接第一个节点
3. **一键开关控制**：安装后，可通过开关实体随时启用或禁用代理

## 使用方法

### 开关实体

安装后会创建一个开关实体：`switch.clash_proxy`，可用于控制代理的启用和禁用。

### 可用服务

#### clash_proxy.update_config

更新Clash配置和订阅

参数：
- `subscription_url`：新的订阅地址URL（可选）

#### clash_proxy.toggle_proxy

启用或禁用Clash代理

参数：
- `enabled`：是否启用代理（必填，布尔值）

### 代理设置

在其他设备上使用代理时，配置如下：

- **HTTP代理**：
  - 地址：您的Home Assistant IP地址
  - 端口：7890

- **SOCKS代理**：
  - 地址：您的Home Assistant IP地址
  - 端口：7891

## 常见问题

**Q: 如何获取Clash订阅地址？**  
A: 您需要从您的代理服务提供商获取Clash格式的订阅地址。

**Q: 集成安装后无法启动怎么办？**  
A: 请检查您的订阅地址是否正确。查看Home Assistant日志以获取更多信息。

**Q: 如何更新代理节点？**  
A: 集成会根据您设置的更新间隔自动更新订阅。您也可以调用`clash_proxy.update_config`服务手动更新，或重启集成触发更新。

**Q: 安装后在集成页面找不到Clash Proxy怎么办？**  
A: 尝试搜索"clash"或"proxy"关键词，或者检查是否有错误日志。确保在HACS安装后已重启Home Assistant。

**Q: 无法找到Super代理组怎么办？**  
A: 确保您的订阅配置中包含名称中带有"super"关键字的代理组。如果没有找到，集成会使用默认配置。

## 隐私说明

此集成只会将您的配置发送到您提供的订阅地址，不会收集或发送任何其他数据。所有代理流量都是在本地处理的，不会经过任何第三方服务器。

## 许可证

MIT 