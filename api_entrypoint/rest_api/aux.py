import hashlib


def create_hash_md5(value: str) -> str:
    """
        Create a hash based on a given :value
        based on the md5 algorithm.
    """
    md5_hash = hashlib.md5()
    md5_hash.update(value.encode('utf-8'))
    return str(md5_hash.hexdigest())
