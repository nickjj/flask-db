.PHONY: help
help:
	@printf "%s\n" "Useful targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  make %-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install package to dev environment
	pip3 install --user --editable .

.PHONY: uninstall
uninstall: ## Uninstall package from dev environment
	python3 setup.py develop --user -u

.PHONY: clean
clean: ## Remove build related files
	python3 setup.py sdist clean --all
	rm -rf build/ dist/ *.egg-info/

.PHONY: build
build: ## Build package and wheel
	python3 setup.py sdist bdist_wheel

.PHONY: publish
publish: ## Publish package to PyPI
	python3 setup.py sdist upload
