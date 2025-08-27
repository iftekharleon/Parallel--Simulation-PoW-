
#!/usr/bin/env bash
set -euo pipefail
python -m ppowsim.cli mine --blocks 3 --difficulty-bits 20 --workers 4 --mode threading --seed 42
python -m ppowsim.cli bench --workers 1 2 4 --blocks 6 --difficulty-bits 20 --mode multiprocessing --out bench.csv --seed 123
python -m ppowsim.cli plot bench.csv
