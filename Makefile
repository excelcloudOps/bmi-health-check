.PHONY: test run build
test:
	PYTHONPATH=. pytest -q

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080

build:
	docker build -t bmi-health-check .
