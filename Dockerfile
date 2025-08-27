
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY README.md .

# Default command mines a few blocks with multiprocessing
CMD ["python", "-m", "ppowsim.cli", "mine", "--blocks", "3", "--difficulty-bits", "20", "--workers", "4", "--mode", "multiprocessing"]
