SRC = $(wildcard notebooks/*.ipynb)

all: clean dist site

airt: $(SRC) settings.ini .install_pre_commit_hooks
	touch README.md
	nbdev_export
	touch airt

sast: .sast_bandit .sast_semgrep

.sast_bandit: airt
	bandit -r airt
	touch .sast_bandit

.sast_semgrep: airt
	semgrep --config auto --error airt
	touch .sast_semgrep

trivy_scan_repo:
	./scripts/trivy_scan_repo.sh

site: dist
	nbdev_mkdocs docs
	touch mkdocs/site

docs_serve: site
	nbdev_mkdocs preview --port 6007

empty_bucket:
	aws s3 ls | cut -d' ' -f3- | grep "^${STORAGE_BUCKET_PREFIX}" | xargs -I {} aws s3 rb --force s3://{}
	az login --service-principal --username ${AZURE_CLIENT_ID} --tenant ${AZURE_TENANT_ID} --password ${AZURE_CLIENT_SECRET}
	az storage account list --query "[*].name" -o tsv | grep "^${AZURE_STORAGE_ACCOUNT_PREFIX}" | xargs -I {} az storage account delete --yes --name {} --resource-group ${AZURE_RESOURCE_GROUP}

test: mypy dist empty_bucket
	nbdev_test --timing --do_print --pause 1

pypi: dist
	twine upload --repository pypi dist/*

export PATH := $(HOME)/.local/bin:$(PATH)

dist: airt
	python3 setup.py sdist bdist_wheel
	pip install -e '.[dev]'
	touch dist
    
clean:
	rm -rf mkdocs/docs/ mkdocs/site/
	rm -rf airt
	rm -rf airt.egg-info
	rm -rf build
	rm -rf dist
	pip uninstall airt -y

mypy: airt
	mypy airt --ignore-missing-imports
    
check_secrets: .add_allowed_git_secrets
	git secrets --scan -r

check: mypy check_secrets detect_secrets sast trivy_scan_repo

.install_git_secrets_hooks:
	git secrets --install -f
	git secrets --register-aws
	touch .install_git_secrets_hooks

.add_allowed_git_secrets: .install_git_secrets_hooks allowed_secrets.txt
	git secrets --add -a "dummy"
	git config --unset-all secrets.allowed
	cat allowed_secrets.txt | xargs -I {} git secrets --add -a {}
	touch .add_allowed_git_secrets

check_git_history_for_secrets: .add_allowed_git_secrets
	git secrets --scan-history

.install_pre_commit_hooks:
	pre-commit install
	touch .install_pre_commit_hooks

detect_secrets: .install_pre_commit_hooks
	git ls-files -z | xargs -0 detect-secrets-hook --baseline .secrets.baseline

.PHONY: prepare
prepare: all check test
	nbdev_clean
