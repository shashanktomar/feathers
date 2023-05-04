##@ General

# The help target prints out all targets with their descriptions organized
# beneath their categories. The categories are represented by '##@' and the
# target descriptions by '##'. The awk commands is responsible for reading the
# entire set of makefiles included in this invocation, looking for lines of the
# file as xyz: ## something, and then pretty-format the target and help. Then,
# if there's a line with ##@ something, that gets pretty-printed as a category.
# More info on the usage of ANSI control characters for terminal formatting:
# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters
# More info on the awk command:
# http://linuxcommand.org/lc3_adv_awk.php

help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Poetry Targets
install: ## install all dependencies
	poetry install --sync

update: ## update deps
	poetry update

##@ Linting Targets
lint-ruff: ## ruff check
	poetry run ruff check .

lint-black: ## black check
	poetry run black --check .

lint-mypy: ## black check
	poetry run mypy --pretty .

lint: lint-ruff lint-black lint-mypy ## check for linting errors using ruff, black and mypy

fix-dry-run: ## show fixes that will be made by ruff and black
	poetry run ruff check --diff . && poetry run black --diff --color .

fix: ## fix linting errors using ruff and black
	poetry run black . && poetry run ruff check --fix .

##@ Test Targets
test: ## test
	poetry run pytest

##@ Execution Targets
.PHONY: app
demo: ## Run demo
	python -m textual_pixels 

console: ## Run dev console
	textual console

##@ Release Targets
publish: ## publish to pypi
	poetry publish --build
