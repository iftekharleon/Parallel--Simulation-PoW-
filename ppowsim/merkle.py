
from .utils import sha256_hex

# Simplified merkle root (not a true merkle tree for speed)
def simple_merkle_root_hex(txs: list[str]) -> str:
    if not txs:
        return "00" * 32
    joined = ("|".join(txs)).encode("utf-8")
    return sha256_hex(joined)
