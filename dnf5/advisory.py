import libdnf5.base as dnf  # noqa: F401

from libdnf5.rpm import PackageQuery, Package  # noqa: F401
from libdnf5.repo import RepoQuery, Repo  # noqa : F401
from libdnf5.common import QueryCmp_NEQ, QueryCmp_NOT_IGLOB, QueryCmp_ICONTAINS, QueryCmp_IGLOB, QueryCmp_GT,QueryCmp_EQ
from libdnf5.advisory import AdvisoryQuery, Advisory,AdvisoryPackage,AdvisoryReference
from zstandard import backend


class Backend(dnf.Base):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        # Yumex is run as user, force it to use user cache instead of systems
        # This allows it to refresh the metadata correctly.
        # It already does the same thing in DNF4
        cache_directory = self.get_config().get_cachedir_option().get_value()
        self.get_config().get_system_cachedir_option().set(cache_directory)

        self.load_config()
        self.setup()
        self.reset_backend()

    def reset_backend(self) -> None:
        self.repo_sack = self.get_repo_sack()
        self.repo_sack.create_repos_from_system_configuration()
        # FIXME: should be cleaned up when dnf5 5.1.x support is not needed
        try:
            self.repo_sack.load_repos()  # dnf5 5.2.0
        except Exception:
            self.repo_sack.update_and_load_enabled_repos(True)  # dnf5 5.1.x

def main():
    dnf_backend = Backend()
    query = PackageQuery(dnf_backend)
    query.filter_installed()
    query.filter_name(["fakeroot-libs"])
    print(list(query))
    adv_query = AdvisoryQuery(dnf_backend)
    adv_pkgs:list[AdvisoryPackage] = list(adv_query.get_advisory_packages_sorted(query))
    for adv_pkg in adv_pkgs:
        print(adv_pkg.get_name())
        advisory:Advisory = adv_pkg.get_advisory()
        print(advisory.get_title())
        print(advisory.get_description())
        print(advisory.get_type())
        refs:list[AdvisoryReference] = list(advisory.get_references())
        print("# Refs:",len(refs))
        for ref in refs:
            print(ref)
if __name__ == "__main__":
    main()