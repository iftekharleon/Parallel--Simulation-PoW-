import time
from .miner import mine_block_parallel
from .blockchain import Blockchain, Block
import matplotlib.pyplot as plt

def run_benchmark(num_blocks=5, difficulty_bits=20, max_workers=8, mode="multiprocessing"):
    blockchain = Blockchain()
    results = []

    for workers in range(1, max_workers + 1):
        print(f"\n⚡ Running with {workers} workers...")
        start_time = time.time()

        for _ in range(num_blocks):
            last_block = blockchain.chain[-1]
            result = mine_block_parallel(
                index=last_block.index + 1,
                previous_hash=last_block.hash,
                timestamp=time.time(),
                data="benchmark block",
                difficulty_bits=difficulty_bits,
                max_workers=workers,
                mode=mode,
            )

            new_block = Block(
                last_block.index + 1,
                time.time(),
                "benchmark block",
                result["hash"],
                result["nonce"],
                last_block.hash,
            )
            blockchain.add_block(new_block)

        end_time = time.time()
        results.append((workers, end_time - start_time))

    return results

def plot_results(results):
    workers, times = zip(*results)
    plt.plot(workers, times, marker="o")
    plt.xlabel("Number of Workers")
    plt.ylabel("Time (s)")
    plt.title("Benchmark: Parallel PoW Mining")
    plt.grid(True)
    plt.show()
