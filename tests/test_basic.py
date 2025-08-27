
from ppowsim.blockchain import build_candidate, verify_chain
from ppowsim.mempool import fake_tx_pool
from ppowsim.mining import mine_threading

def test_mine_one_block():
    pool = fake_tx_pool(100, seed=1)
    cand = build_candidate(None, pool, k=50, difficulty_bits=18, timestamp=0)
    res = mine_threading(cand, workers=2)
    assert res.found
    assert cand.hash_hex is not None
    assert verify_chain([cand])
