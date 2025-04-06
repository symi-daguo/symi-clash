"""Clash客户端实现"""
import logging
import os
import platform
import subprocess
import requests
import tempfile
import threading
import time
import urllib.request
from typing import Any, Dict

_LOGGER = logging.getLogger(__name__)

class ClashClient:
    """Clash客户端"""

    def __init__(
        self,
        subscription_url: str,
        proxy_mode: str = "rule",
        allow_lan: bool = True,
        log_level: str = "info",
        auto_update: bool = True,
        update_interval: int = 12,
    ):
        """初始化Clash客户端"""
        self.subscription_url = subscription_url
        self.proxy_mode = proxy_mode
        self.allow_lan = allow_lan
        self.log_level = log_level
        self.auto_update = auto_update
        self.update_interval = update_interval
        self.process = None
        self.config_path = None
        self.executable_path = self._get_executable_path()
        self.running = False
        self.update_thread = None
        self.stop_update = threading.Event()
        self.stats = {
            "upload": 0,
            "download": 0,
            "connections": 0,
            "latency": {}
        }

    def _get_executable_path(self) -> str:
        """获取可执行文件路径"""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        binary_dir = os.path.join(base_dir, "bin")
        os.makedirs(binary_dir, exist_ok=True)
        
        if system == "windows":
            executable = os.path.join(binary_dir, "clash.exe")
        else:
            executable = os.path.join(binary_dir, "clash")
        
        # 检查可执行文件是否存在，不存在则下载
        if not os.path.exists(executable):
            self._download_clash_binary(executable, system, machine)
        
        return executable

    def _download_clash_binary(self, executable_path: str, system: str, machine: str) -> None:
        """下载Clash二进制文件"""
        # 根据系统和架构选择下载链接
        version = "v1.18.0"
        
        arch_map = {
            "x86_64": "amd64",
            "amd64": "amd64",
            "i386": "386",
            "i686": "386",
            "armv7l": "armv7",
            "armv6l": "armv6",
            "aarch64": "arm64",
            "arm64": "arm64",
        }
        
        arch = arch_map.get(machine, "amd64")
        
        if system == "windows":
            download_url = f"https://github.com/Dreamacro/clash/releases/download/{version}/clash-{system}-{arch}-{version}.zip"
            # 下载并解压缩
            try:
                temp_file = os.path.join(os.path.dirname(executable_path), "clash.zip")
                urllib.request.urlretrieve(download_url, temp_file)
                # 解压缩并设置可执行权限
                import zipfile
                with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                    zip_ref.extractall(os.path.dirname(executable_path))
                os.remove(temp_file)
            except Exception as e:
                _LOGGER.error("下载Clash失败: %s", str(e))
                raise
        else:
            download_url = f"https://github.com/Dreamacro/clash/releases/download/{version}/clash-{system}-{arch}-{version}.gz"
            # 下载并解压缩
            try:
                temp_file = os.path.join(os.path.dirname(executable_path), "clash.gz")
                urllib.request.urlretrieve(download_url, temp_file)
                # 解压缩
                import gzip
                import shutil
                with gzip.open(temp_file, 'rb') as f_in:
                    with open(executable_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(temp_file)
                # 设置可执行权限
                os.chmod(executable_path, 0o755)
            except Exception as e:
                _LOGGER.error("下载Clash失败: %s", str(e))
                raise

    def _generate_config(self) -> str:
        """生成Clash配置文件"""
        # 下载订阅配置
        try:
            response = requests.get(self.subscription_url, timeout=30)
            if response.status_code != 200:
                _LOGGER.error("下载订阅失败: %s", response.status_code)
                raise Exception(f"下载订阅失败: {response.status_code}")
                
            config_content = response.text
            
            # 创建临时配置文件
            fd, config_path = tempfile.mkstemp(suffix=".yaml")
            with os.fdopen(fd, "w") as f:
                f.write(config_content)
                
            # 添加或修改一些配置项
            # 这里可以进一步修改配置，如端口、允许局域网访问等
                
            return config_path
            
        except Exception as e:
            _LOGGER.error("生成配置失败: %s", str(e))
            raise

    def start(self) -> None:
        """启动Clash"""
        if self.running:
            return
            
        try:
            # 获取配置文件路径
            self.config_path = self._generate_config()
            
            # 启动Clash进程
            cmd = [
                self.executable_path,
                "-f", self.config_path,
                "-d", os.path.dirname(self.config_path)
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 等待启动成功
            time.sleep(1)
            if self.process.poll() is not None:
                stdout, stderr = self.process.communicate()
                raise Exception(f"启动Clash失败: {stderr}")
                
            self.running = True
            
            # 启动自动更新线程
            if self.auto_update:
                self.stop_update.clear()
                self.update_thread = threading.Thread(target=self._auto_update_thread)
                self.update_thread.daemon = True
                self.update_thread.start()
                
            _LOGGER.info("Clash代理已成功启动")
            
        except Exception as e:
            _LOGGER.error("启动Clash失败: %s", str(e))
            self.stop()
            raise

    def stop(self) -> None:
        """停止Clash"""
        # 停止自动更新线程
        if self.update_thread and self.update_thread.is_alive():
            self.stop_update.set()
            self.update_thread.join(timeout=1)
            
        # 停止Clash进程
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
            
        # 删除临时配置文件
        if self.config_path and os.path.exists(self.config_path):
            try:
                os.remove(self.config_path)
            except OSError:
                pass
            self.config_path = None
            
        self.running = False
        _LOGGER.info("Clash代理已停止")

    def update_config(self, subscription_url: str = None) -> None:
        """更新配置"""
        if subscription_url:
            self.subscription_url = subscription_url
            
        if not self.running:
            return
            
        try:
            # 生成新的配置文件
            new_config_path = self._generate_config()
            
            # 重新启动Clash
            self.stop()
            self.config_path = new_config_path
            self.start()
            
        except Exception as e:
            _LOGGER.error("更新配置失败: %s", str(e))
            # 如果更新失败，尝试使用旧配置重新启动
            if not self.running and self.config_path:
                self.start()

    def set_enabled(self, enabled: bool) -> None:
        """设置是否启用代理"""
        if enabled and not self.running:
            self.start()
        elif not enabled and self.running:
            self.stop()

    def _auto_update_thread(self) -> None:
        """自动更新线程"""
        while not self.stop_update.is_event_set():
            # 等待指定的更新间隔
            for _ in range(self.update_interval * 60 * 60):  # 转换为秒
                if self.stop_update.wait(1):  # 每秒检查一次是否应该停止
                    return
            
            # 更新配置
            try:
                self.update_config()
            except Exception as e:
                _LOGGER.error("自动更新失败: %s", str(e))

    def get_status(self) -> Dict[str, Any]:
        """获取Clash状态"""
        status = {
            "running": self.running,
            "subscription_url": self.subscription_url,
            "proxy_mode": self.proxy_mode,
            "allow_lan": self.allow_lan,
            "log_level": self.log_level,
            "auto_update": self.auto_update,
            "update_interval": self.update_interval,
            "stats": self.stats
        }
        
        # 如果正在运行，尝试从API获取更多信息
        if self.running:
            try:
                # 从Clash API获取状态信息
                # 这里可以添加更多API调用获取更详细的信息
                pass
            except Exception as e:
                _LOGGER.error("获取Clash状态失败: %s", str(e))
                
        return status 