
from __future__ import annotations
import time, threading, multiprocessing as mp
from dataclasses import dataclass
from .blockchain import Block, is_valid_pow, target_from_bits
from .utils import sha256_hex

@dataclass
class MineResult:
    found: bool
    nonce: int
    hash_hex: str
    attempts: int
    duration: float

def _hash_header_with_nonce(header, nonce: int) -> str:
    header.nonce = nonce
    return header.hash_hex()

# ---------------- Threading ----------------

def _worker_thread(worker_id: int, header_snapshot, start_nonce: int, stride: int, bits: int,
                   found_event: threading.Event, result_box: dict, attempts_box: list[int]):
    # header_snapshot is a shallow copy with the fixed fields; only nonce mutates locally
    local_attempts = 0
    target = target_from_bits(bits)
    nonce = start_nonce
    while not found_event.is_set():
        h = _hash_header_with_nonce(header_snapshot, nonce)
        local_attempts += 1
        if int(h, 16) < target:
            # publish result once
            if not found_event.is_set():
                result_box["found"] = True
                result_box["nonce"] = nonce
                result_box["hash_hex"] = h
                found_event.set()
            break
        nonce += stride
    attempts_box[worker_id] = local_attempts

def mine_threading(block: Block, workers: int, base_nonce: int = 0) -> MineResult:
    header_copy = type(block.header)(**vars(block.header))  # copy
    found_event = threading.Event()
    result_box = {"found": False, "nonce": 0, "hash_hex": ""}
    attempts_box = [0] * workers

    t0 = time.perf_counter()
    threads = []
    for wid in range(workers):
        th = threading.Thread(target=_worker_thread,
                              args=(wid, type(header_copy)(**vars(header_copy)), base_nonce + wid, workers,
                                    block.header.difficulty_bits, found_event, result_box, attempts_box))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
    dt = time.perf_counter() - t0

    if not result_box["found"]:
        return MineResult(False, 0, "", sum(attempts_box), dt)

    # finalize block
    block.header.nonce = result_box["nonce"]
    block.finalize()
    return MineResult(True, block.header.nonce, block.hash_hex, sum(attempts_box), dt)

# ---------------- Multiprocessing ----------------

def _worker_proc(header_dict: dict, start_nonce: int, stride: int, bits: int,
                 found: mp.Event, result: mp.Dict, attempts: mp.Array):
    from .blockchain import BlockHeader
    hdr = BlockHeader(**header_dict)
    target = target_from_bits(bits)
    local_attempts = 0
    nonce = start_nonce
    while not found.is_set():
        hdr.nonce = nonce
        h = hdr.hash_hex()
        local_attempts += 1
        if int(h, 16) < target:
            if not found.is_set():
                result["found"] = True
                result["nonce"] = nonce
                result["hash_hex"] = h
                found.set()
            break
        nonce += stride
    attempts.append(local_attempts)

def mine_multiprocessing(block: Block, workers: int, base_nonce: int = 0) -> MineResult:
    header_dict = vars(block.header).copy()
    with mp.Manager() as mgr:
        found = mgr.Event()
        result = mgr.dict()
        attempts = mgr.list()
        t0 = time.perf_counter()
        procs = []
        for wid in range(workers):
            p = mp.Process(target=_worker_proc, args=(header_dict, base_nonce + wid, workers,
                                                      block.header.difficulty_bits, found, result, attempts))
            p.start()
            procs.append(p)
        for p in procs:
            p.join()
        dt = time.perf_counter() - t0

        total_attempts = sum(int(x) for x in attempts)
        if not result.get("found", False):
            return MineResult(False, 0, "", total_attempts, dt)

        block.header.nonce = int(result["nonce"])
        block.finalize()
        return MineResult(True, block.header.nonce, block.hash_hex, total_attempts, dt)
