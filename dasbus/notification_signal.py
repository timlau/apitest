# Send a notication using freedesktop Notification API
#
# https://specifications.freedesktop.org/notification-spec/latest/ar01s09.html

from os import name
from dasbus.connection import SessionMessageBus
from dasbus.identifier import DBusServiceIdentifier
from dasbus.loop import EventLoop

NOTIFICATION_NAMESPACE = ("org", "freedesktop", "Notifications")
NOTIFICATION = DBusServiceIdentifier(namespace=NOTIFICATION_NAMESPACE, message_bus=SessionMessageBus())


def send_notification(app_name, icon_name, summary, body, actions=[], hints={}, timeout=0):
    proxy = NOTIFICATION.get_proxy()
    id = proxy.Notify(app_name, 0, icon_name, summary, body, actions, hints, timeout)
    print("The notification {} was sent.".format(id))
    return id


def on_action_invoked(*args):
    print(f"SIGNAL:ActionInvoked {args}")


def on_activation_token(*args):
    print(f"SIGNAL:ActivationToken {args}")


def main():
    app_name = "Yum Extender"
    icon_name = "software-update-available-symbolic"
    summary = "Updates is available"
    body = "this is the body of the notifcation"
    action = ["open", "Open Package Manager"]
    send_notification(app_name, icon_name, summary, body, actions=action)
    proxy = NOTIFICATION.get_proxy()
    proxy.ActionInvoked.connect(on_action_invoked)
    proxy.ActivationToken.connect(on_activation_token)
    loop = EventLoop()
    loop.run()


if __name__ == "__main__":
    main()
