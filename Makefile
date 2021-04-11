black:
	black setup.py planscore_cli

live: black
	python setup.py sdist upload

.PHONY: live black