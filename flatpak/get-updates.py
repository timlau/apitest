import gi
gi.require_version('Flatpak', '1.0')
from gi.repository import Flatpak # type: ignore 

user_upd = len(Flatpak.Installation.new_user().list_installed_refs_for_update())
system_upd = len(Flatpak.Installation.new_system().list_installed_refs_for_update())

print(f"User updates : {user_upd}")
print(f"System updates : {system_upd}")