# ⛏️ Parallel Proof-of-Work Simulator (ppowsim)

A lightweight Python simulator for **Proof-of-Work (PoW) blockchain mining**, with support for **parallelized mining** using multiprocessing.  
This project helps understand how mining difficulty, number of workers, and execution mode affect mining performance.

---

## 📌 Features
- Simulates a **basic blockchain** with proof-of-work.
- Mines blocks either:
  - **Sequentially** (single worker).
  - **Parallelized** (multiple workers using Python's `multiprocessing`).
- **Benchmarking module** to measure mining performance across:
  - Different worker counts.
  - Difficulty levels.
  - Execution modes (`sequential` vs `parallel`).
- Command-line interface (CLI) with `click`.

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/parallel-pow-sim.git
cd parallel-pow-sim

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
python -m ppowsim.cli --help
## Mine blocks
python -m ppowsim.cli mine --blocks 5 --difficulty 18 --workers 4 --mode parallel

#Run benchmarks
python -m ppowsim.cli benchmark --blocks 5 --difficulty 18 --max-workers 8 --mode parallel
