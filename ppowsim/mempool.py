
import random

def fake_tx_pool(n: int = 1000, seed: int | None = None) -> list[str]:
    rd = random.Random(seed)
    txs = []
    for i in range(n):
        a = rd.randint(100000, 999999)
        b = rd.randint(100000, 999999)
        amt = rd.random() * 10
        txs.append(f"{a}->{b}:{amt:.6f}")
    return txs

def select_txs(pool: list[str], k: int = 100) -> list[str]:
    if len(pool) <= k:
        return pool.copy()
    # Deterministic pick for reproducibility: take first k
    return pool[:k]
