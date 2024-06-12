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

    def find_pkg_by_name(self, name):
        query:list[Package] = PackageQuery(self)
        query.filter_installed()
        query.filter_name([name])
        return query
    

def list_files(query):
    for pkg in query:
        print(f"{pkg.get_nevra()}")
        filelist = pkg.get_files()
        for file in filelist:
            print(f"  --> {file}") 


def main():
    dnf_backend = Backend()
    query = dnf_backend.find_pkg_by_name("fakeroot-libs")
    list_files(query)
    query = dnf_backend.find_pkg_by_name("abseil-cpp")
    list_files(query)

if __name__ == "__main__":
    main()