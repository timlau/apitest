from dasbus.connection import SessionMessageBus
from dasbus.error import DBusError
from dasbus.identifier import DBusServiceIdentifier
from dasbus.typing import get_native

SYSTEMD_NAMESPACE = (
    "org", "freedesktop", "systemd1"
)

YUMEX_UPDATER_NAMESPACE = (
    "com","yumex", "UpdateService"
)

SYSTEMD = DBusServiceIdentifier(
    namespace=SYSTEMD_NAMESPACE,
    message_bus=SessionMessageBus()
)

YUMEX_UPDATER = DBusServiceIdentifier(
    namespace=YUMEX_UPDATER_NAMESPACE,
    message_bus=SessionMessageBus()
)

def is_user_service_running(service_name):
    try:
        systemd = SYSTEMD.get_proxy(interface_name="org.freedesktop.systemd1.Manager")
        unit_path = systemd.GetUnit(service_name)
        print(unit_path)
        unit = SYSTEMD.get_proxy(unit_path)
        state = get_native(unit.Get("org.freedesktop.systemd1.Unit", "SubState"))
        print(state)
        return state == "running"
    except DBusError as e:
        print(e)
        return False

def sync_updates():
    service_name = "yumex-updater-systray.service"

    if is_user_service_running(service_name):
        try:
            updater = YUMEX_UPDATER.get_proxy()
            updater.RefreshUpdates()
            print("(sync_updates) triggered updater checker refresh")
        except DBusError as e:
            print(f"(sync_updates) DBusException: {e}")
            # Handle the exception or log it as needed
    else:
        print(f"(sync_updates) The service {service_name} is not running.")

if __name__ == "__main__":
    sync_updates()