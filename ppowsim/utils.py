
import hashlib, struct, time, json, os, random

def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def now_ts() -> float:
    return time.time()

def random_seed(seed: int | None):
    if seed is not None:
        random.seed(seed)
        os.environ["PYTHONHASHSEED"] = str(seed)

def int_to_bytes_be(i: int, length: int) -> bytes:
    return i.to_bytes(length, "big", signed=False)

def pack_u32(i: int) -> bytes:
    return struct.pack(">I", i)

def pack_u64(i: int) -> bytes:
    return struct.pack(">Q", i)

def dump_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
