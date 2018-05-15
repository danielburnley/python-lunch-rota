.PHONY: test

test:
	env PYTHONPATH=. pytest

deploy:
	./bin/deploy.sh
