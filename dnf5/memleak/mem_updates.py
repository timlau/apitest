# Test dnf metadata mem-leak
#
# requirements:
# dnf5 install python3-memray
#
# run with:
#
# /bin/python -m memray run --live ./dnf5/mem_updates.py



import time
import subprocess
import shlex

import libdnf5 as dnf


def check_updates():
    base = dnf.base.Base()
    try:
        # Setup dnf base
        cache_directory = base.get_config().get_cachedir_option().get_value()
        base.get_config().get_system_cachedir_option().set(cache_directory)
        base.load_config()
        base.setup()
        # Setup repositories
        base.repo_sack = base.get_repo_sack()
        base.repo_sack.create_repos_from_system_configuration()
        base.repo_sack.update_and_load_enabled_repos(True)
        # Get availble updates
        updates = dnf.rpm.PackageQuery(base)
        updates.filter_upgrades()
        updates.filter_arch(["src"], dnf.common.QueryCmp_NEQ)
        updates.filter_latest_evr()
        return len(list(updates))
    finally:
        del base.repo_sack
        del base


def main():
    expire_cmd=shlex.split("dnf5 clean expire-cache")
    print(expire_cmd)
    for x in range(3):
        print(check_updates())
        time.sleep(5)
    for x in range(3):
        subprocess.call(expire_cmd, shell=False)
        time.sleep(2)
        print(check_updates())
        time.sleep(5)
    time.sleep(20)
    

if __name__ == "__main__":
    main()