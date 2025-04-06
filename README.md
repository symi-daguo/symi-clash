# Clash Proxy for Home Assistant

这是一个为 Home Assistant 设计的 Clash 代理服务集成，只需提供订阅地址，即可在 Home Assistant 中使用代理服务。符合2025年Home Assistant集成标准。

## 功能特点

- 简单易用：只需输入订阅地址，无需复杂配置
- 完全集成：作为 Home Assistant 集成运行，通过HACS安装
- 支持多种代理协议：Shadowsocks、V2Ray、Trojan 等
- 自动更新：定时自动更新订阅配置
- 易于管理：提供开关实体和服务调用接口

## 安装方法

### 使用HACS安装（推荐）

1. 确保已安装 [HACS](https://hacs.xyz/)
2. 在HACS中添加自定义仓库：
   - 类型: 集成
   - URL: `https://github.com/symi-daguo/symi-clash`
3. 在HACS中搜索并安装 "Clash Proxy"
4. 重启 Home Assistant
5. 在集成页面添加 "Clash代理" 集成

### 手动安装

1. 下载此仓库
2. 将 `custom_components/clash_proxy` 目录复制到您的 Home Assistant 配置目录的 `custom_components` 文件夹中
3. 重启 Home Assistant
4. 在集成页面添加 "Clash代理" 集成

## 配置说明

添加集成时需要配置以下参数：

- **订阅地址**：您的Clash配置订阅地址（必填）
- **代理模式**：rule(规则模式)、global(全局模式)、direct(直连模式)
- **允许局域网访问**：是否允许局域网设备使用代理
- **日志级别**：info、debug、warning、error、silent
- **自动更新**：是否启用自动更新订阅
- **更新间隔**：自动更新的时间间隔（小时）

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

## 隐私说明

此集成只会将您的配置发送到您提供的订阅地址，不会收集或发送任何其他数据。所有代理流量都是在本地处理的，不会经过任何第三方服务器。

## 许可证

MIT 