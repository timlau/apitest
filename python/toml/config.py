from dataclasses import dataclass
import tomllib
import shutil
import logging
from pathlib import Path

# Setup logger
logger = logging.getLogger("yumex_updater")
logging.basicConfig(
    level=logging.DEBUG,
    format="(%(name)-5s) -  %(message)s",
    datefmt="%H:%M:%S",
)


@dataclass
class Config:
    custom_updater: str
    always_hide: bool
    update_sync_interval: int
    send_notification: bool

    @classmethod
    def from_file(cls):
        config_dir = Path.home() / ".config" / "yumex"
        default_config_path = "/usr/share/yumex/yumex-service.conf"
        user_config_path = config_dir / "yumex-service.conf"
        # Create the config directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        # Copy the default config file if the user config file doesn't exist
        if not user_config_path.exists():
            shutil.copy(default_config_path, user_config_path)
        logger.debug(f"config path: {user_config_path}")

        with user_config_path.open("rb") as f:
            data = tomllib.load(f)

        custom_updater = data.get("custom_updater", None)
        always_hide = data.get("always_hide", False)
        update_sync_interval = data.get("update_sync_interval", 3600)
        notification = data.get("send_notification", True)
        logger.debug(f"CONFIG: custom_updater        = {custom_updater}")
        logger.debug(f"CONFIG: always_hide           = {always_hide}")
        logger.debug(f"CONFIG: update_sync_interval  = {update_sync_interval}")
        logger.debug(f"CONFIG: send_notification     = {notification}")
        return cls(custom_updater, always_hide, update_sync_interval, notification)


if __name__ == "__main__":
    config = Config.from_file()
