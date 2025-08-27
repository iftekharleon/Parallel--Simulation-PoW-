
from __future__ import annotations
import csv, pathlib
from dataclasses import asdict
from .blockchain import build_candidate, verify_chain, Block
from .mempool import fake_tx_pool, select_txs
from .mining import mine_threading, mine_multiprocessing, MineResult
from .utils import now_ts, dump_json

def mine_n_blocks(n_blocks: int, difficulty_bits: int, workers: int, mode: str, seed: int | None):
    pool = fake_tx_pool(2000, seed=seed)
    chain: list[Block] = []
    miner = mine_threading if mode == "threading" else mine_multiprocessing
    for i in range(n_blocks):
        prev = chain[-1] if chain else None
        ts = now_ts()
        cand = build_candidate(prev, pool, k=100, difficulty_bits=difficulty_bits, timestamp=ts)
        result = miner(cand, workers=workers)
        if not result.found:
            raise RuntimeError("Mining failed to find a nonce")
        chain.append(cand)
    assert verify_chain(chain), "Chain verification failed after mining"
    return chain

def write_csv(path: str, rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

def bench(workers_list: list[int], n_blocks: int, difficulty_bits: int, mode: str, out_csv: str, seed: int | None):
    pool = fake_tx_pool(5000, seed=seed)
    rows = []
    from .utils import now_ts
    from .blockchain import build_candidate, Block
    miner = mine_threading if mode == "threading" else mine_multiprocessing

    prev: Block | None = None
    for w in workers_list:
        for b in range(n_blocks):
            ts = now_ts()
            cand = build_candidate(prev, pool, k=100, difficulty_bits=difficulty_bits, timestamp=ts)
            res = miner(cand, workers=w)
            rows.append({
                "workers": w,
                "block_index": cand.header.index,
                "nonce": cand.header.nonce,
                "hash_hex": cand.hash_hex,
                "attempts": res.attempts,
                "duration_s": f"{res.duration:.6f}",
                "difficulty_bits": difficulty_bits,
                "mode": mode,
            })
            prev = cand
    write_csv(out_csv, rows)
    return out_csv

def save_chain_json(path: str, chain: list[Block]):
    dump_json(path, [{
        "header": {
            "index": b.header.index,
            "prev_hash_hex": b.header.prev_hash_hex,
            "timestamp": b.header.timestamp,
            "merkle_root_hex": b.header.merkle_root_hex,
            "difficulty_bits": b.header.difficulty_bits,
            "nonce": b.header.nonce,
        },
        "txs": b.txs,
        "hash_hex": b.hash_hex,
    } for b in chain])
