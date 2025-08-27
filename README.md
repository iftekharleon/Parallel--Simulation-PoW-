
# Parallel PoW Blockchain Simulator (ppowsim)

A complete, production-ready educational project to explore **parallel mining** for Proof-of-Work (PoW).  
It supports **threading** and **multiprocessing**, a clean CLI, benchmarking to CSV, and optional plots.

## Features
- Minimal blockchain with PoW
- Parallel mining (threads or processes) with non-overlapping nonce search
- Deterministic candidate block construction
- Benchmark harness: runs multiple blocks and thread/process counts
- CSV logs + optional plotting
- Chain verification
- Dockerized for easy runs

## Quickstart

### Local (Python 3.10+)
```bash
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m ppowsim.cli mine --blocks 3 --difficulty-bits 20 --workers 4 --mode threading
python -m ppowsim.cli bench --workers 1 2 4 8 --blocks 10 --difficulty-bits 20 --mode multiprocessing --out bench.csv
python -m ppowsim.cli verify chain.json
```

### Docker
```bash
docker build -t ppowsim .
docker run --rm ppowsim python -m ppowsim.cli mine --blocks 3 --difficulty-bits 20 --workers 4 --mode multiprocessing
```

### Outputs
- `chain.json` — serialized chain after mining
- `bench.csv` — benchmark logs
- `plots/` — optional figures (time vs workers, speedup vs workers)

## CLI commands
- `mine` — mine N sequential blocks and save chain
- `bench` — benchmark across worker counts; write CSV
- `verify` — verify a saved chain file

## Project layout
```
parallel-pow-sim/
  ├─ src/ppowsim/
  │   ├─ __init__.py
  │   ├─ blockchain.py
  │   ├─ mempool.py
  │   ├─ merkle.py
  │   ├─ mining.py
  │   ├─ utils.py
  │   ├─ cli.py
  │   └─ benchmarks.py
  ├─ tests/
  │   └─ test_basic.py
  ├─ scripts/
  │   └─ demo.sh
  ├─ requirements.txt
  ├─ pyproject.toml
  ├─ Dockerfile
  ├─ Makefile
  ├─ README.md
  └─ .gitignore
```

## Notes
- Start with `difficulty-bits` ~ **18–22** for quick runs.
- `--mode multiprocessing` avoids the GIL for real speedups.
- Use `--seed` for reproducible runs.
