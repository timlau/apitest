

def test_fn(p1,p2):
    print(p1,p2)


def wrapper(fn):
    print(fn.__name__)
    fn(1,2)

wrapper(test_fn)