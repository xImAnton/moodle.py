

def check(obj, check_as_dict, **kwargs):
    for k, v in kwargs.items():
        if check_as_dict:
            if obj[k] != v:
                return False
        else:
            if getattr(obj, k) != v:
                return False
    return True


def get(seq, check_as_dict=False, only_one=True, **kwargs):
    out = []
    for item in seq:
        if check(item, check_as_dict, **kwargs):
            if only_one:
                return item
            else:
                out.append(item)
    return None if only_one else out
