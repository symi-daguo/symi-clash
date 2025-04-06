# Clash代理 for Home Assistant

通过这个集成，您可以在Home Assistant中使用Clash代理服务，只需提供订阅地址即可。

## 功能

- 通过简单配置即可使用Clash代理
- 支持多种协议：Shadowsocks、V2Ray、Trojan等
- 自动更新订阅
- 提供开关实体和服务来控制代理

## 使用方法

1. 输入您的Clash订阅地址
2. 配置代理模式和其他选项
3. 使用`switch.clash_proxy`开关控制代理
4. 在您的设备上设置HTTP代理(7890端口)或SOCKS代理(7891端口)

## 配置示例

```yaml
# 配置示例
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1
``` 