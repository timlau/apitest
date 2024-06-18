# Do the same actions as dnf5 --refresh

from pathlib import Path
from libdnf5.base import Base
from libdnf5.repo import RepoCache

base = Base()
# get the repo cache dir
cachedir = Path(base.get_config().get_cachedir_option().get_value())
print(cachedir)
# interate through the repo cachedir
for fn in cachedir.iterdir():
    print(f"Processing repo loacted at {fn}")
    # Setup a RepoCache at the current repo cachedir 
    repo_cache = RepoCache(base,fn.as_posix())
    # expire the cache for the current repo
    repo_cache.write_attribute(RepoCache.ATTRIBUTE_EXPIRED)

