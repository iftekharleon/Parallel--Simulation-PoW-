
.PHONY: mine bench verify clean

mine:
	python -m ppowsim.cli mine --blocks 3 --difficulty-bits 20 --workers 4 --mode multiprocessing

bench:
	python -m ppowsim.cli bench --workers 1 2 4 8 --blocks 8 --difficulty-bits 20 --mode multiprocessing --out bench.csv

verify:
	python -m ppowsim.cli verify chain.json

clean:
	rm -f bench.csv chain.json
	rm -rf __pycache__ src/**/__pycache__ plots
