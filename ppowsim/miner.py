import hashlib
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def compute_hash(index, previous_hash, timestamp, data, nonce):
    block_string = f"{index}{previous_hash}{timestamp}{data}{nonce}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def mine_worker(start_nonce, step, index, previous_hash, timestamp, data, target):
    """
    Worker function that searches for a valid nonce starting at start_nonce
    and incrementing by step (used for parallelism).
    """
    nonce = start_nonce
    while True:
        hash_value = compute_hash(index, previous_hash, timestamp, data, nonce)
        if int(hash_value, 16) < target:
            return nonce, hash_value
        nonce += step

def mine_block_parallel(index, previous_hash, timestamp, data, difficulty_bits, max_workers=4, mode="multiprocessing"):
    """
    Mines a block using parallel workers.
    - index: block index
    - previous_hash: hash of previous block
    - timestamp: time
    - data: block data
    - difficulty_bits: difficulty (higher = harder)
    - max_workers: number of threads/processes
    - mode: "multiprocessing" or "threading"
    """
    target = 2 ** (256 - difficulty_bits)

    Executor = ProcessPoolExecutor if mode == "multiprocessing" else ThreadPoolExecutor

    start_time = time.time()
    with Executor(max_workers=max_workers) as executor:
        futures = []
        for worker_id in range(max_workers):
            futures.append(
                executor.submit(
                    mine_worker,
                    worker_id,  # start nonce
                    max_workers,  # step size
                    index,
                    previous_hash,
                    timestamp,
                    data,
                    target,
                )
            )
        for future in futures:
            result = future.result()
            if result:
                end_time = time.time()
                nonce, hash_value = result
                return {
                    "nonce": nonce,
                    "hash": hash_value,
                    "time": end_time - start_time,
                }
