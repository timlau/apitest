# create a dict from a dataclass

from dataclasses import field, asdict, dataclass


@dataclass
class UpdateInfo():
    id:str
    title:str
    
    def as_dict(self):
        return asdict(self)


if __name__ == "__main__":
    dc = UpdateInfo("name","title")
    print(dc.as_dict())    