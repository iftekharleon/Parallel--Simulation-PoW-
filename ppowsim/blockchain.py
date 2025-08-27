import time
import hashlib
from dataclasses import dataclass

@dataclass
class Block:
    index: int
    previous_hash: str
    timestamp: float
    data: str
    nonce: int = 0
    hash: str = None

    def compute_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self, difficulty_bits=20):
        self.chain = []
        self.difficulty_bits = difficulty_bits
        self.difficulty = 2 ** (256 - difficulty_bits)
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), "Genesis Block")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_block(self, block: Block):
        block.hash = block.compute_hash()
        self.chain.append(block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr.previous_hash != prev.hash:
                return False
            if curr.hash != curr.compute_hash():
                return False
        return True
