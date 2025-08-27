import click
import time
from .blockchain import Blockchain, Block
from .miner import mine_block_parallel
from .benchmark import plot_results, run_benchmark

@click.group()
def cli():
    pass

# ---------------------------
# Mine command
# ---------------------------
@cli.command()
@click.option("--blocks", default=5, help="Number of blocks to mine")
@click.option("--difficulty-bits", default=20, help="Difficulty target bits")
@click.option("--workers", default=4, help="Number of parallel workers")
@click.option("--mode", default="multiprocessing", type=click.Choice(["threading", "multiprocessing"]))
def mine(blocks, difficulty_bits, workers, mode):
    """Mine blocks using parallel PoW."""
    blockchain = Blockchain(difficulty_bits=difficulty_bits)

    for i in range(blocks):
        last_block = blockchain.chain[-1]
        print(f"\n⛏ Mining block {last_block.index + 1}...")
        result = mine_block_parallel(
            index=last_block.index + 1,
            previous_hash=last_block.hash,
            timestamp=time.time(),
            data=f"Block {last_block.index + 1}",
            difficulty_bits=difficulty_bits,
            max_workers=workers,
            mode=mode,
        )

        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            data=f"Block {last_block.index + 1}",
            hash=result["hash"],
            nonce=result["nonce"],
            previous_hash=last_block.hash
        )

        blockchain.add_block(new_block)
        print(f"✅ Block {new_block.index} mined | Nonce: {new_block.nonce} | Hash: {new_block.hash[:16]}...")

# ---------------------------
# Benchmark command (already exists)
# ---------------------------
@cli.command()
@click.option("--blocks", default=5, help="Number of blocks to mine per test")
@click.option("--difficulty-bits", default=20, help="Difficulty target bits")
@click.option("--max-workers", default=8, help="Maximum workers to test")
@click.option("--mode", default="multiprocessing", type=click.Choice(["threading", "multiprocessing"]))
def benchmark(blocks, difficulty_bits, max_workers, mode):
    """Run parallel PoW benchmark and plot results."""
    results = run_benchmark(num_blocks=blocks, difficulty_bits=difficulty_bits, max_workers=max_workers, mode=mode)
    plot_results(results)

if __name__ == "__main__":
    cli()
