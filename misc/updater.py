from dataclasses import dataclass

import gi
gi.require_version("Flatpak", "1.0")
from gi.repository import Flatpak  # type: ignore

from yumex.constants import BACKEND

if BACKEND == "DNF5":
    from yumex.service.dnf5 import check_dnf_updates
else:
    from yumex.service.dnf4 import check_dnf_updates


@dataclass
class Updates:
    sys_update_count: int
    flatpak_user_count: int
    flatpak_sys_count: int

    @classmethod
    def get_updates(cls):
        sys_update_count = len(check_dnf_updates())
        user_installation = Flatpak.Installation.new_user()
        flatpak_user_count = len(user_installation.list_installed_refs_for_update())
        del user_installation

        system_installation = Flatpak.Installation.new_system()
        flatpak_sys_count = len(system_installation.list_installed_refs_for_update())
        del system_installation
        return cls(sys_update_count, flatpak_user_count, flatpak_sys_count)



def main():
    updater:Updates = Updates.get_updates()
    print(updater)

if __name__ == "__main__":
    main()