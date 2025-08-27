# PowerShell script to run Parallel PoW Simulator
# Save this as run.ps1 in project root

Write-Host "=== Setting up environment ==="

# Activate venv (if not already active)
if (-Not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "Virtual environment created."
}

# Use the correct activation script
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
pip install -r requirements.txt

Write-Host "=== Running Parallel PoW Simulator ==="

# Run mining (edit parameters here)
python -m ppowsim.cli mine --blocks 3 --difficulty-bits 20 --workers 4 --mode multiprocessing

Write-Host "=== Done ==="
