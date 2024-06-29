# Send a notication using freedesktop Notification API
#
# https://specifications.freedesktop.org/notification-spec/latest/ar01s09.html

from os import name
from dasbus.connection import SessionMessageBus
from dasbus.error import DBusError
from dasbus.identifier import DBusServiceIdentifier
from dasbus.typing import get_native

NOTIFICATION_NAMESPACE = ("org", "freedesktop", "Notifications")
NOTIFICATION = DBusServiceIdentifier(namespace=NOTIFICATION_NAMESPACE, message_bus=SessionMessageBus())


def send_notification(app_name, icon_name, summary, body, actions=[], hints={}, timeout=0):
    proxy = NOTIFICATION.get_proxy()
    id = proxy.Notify(app_name, 0, icon_name, summary, body, actions, hints, timeout)
    print("The notification {} was sent.".format(id))
    return id


def main():
    app_name = "Yum Extender"
    icon_name = "software-update-available-symbolic"
    summary = "Updates is available"
    body = "this is the body of the notifcation"
    send_notification(app_name, icon_name, summary, body)


if __name__ == "__main__":
    main()
