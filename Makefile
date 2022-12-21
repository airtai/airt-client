SRC = $(wildcard notebooks/*.ipynb)

all: clean dist site

airt: $(SRC) settings.ini .install_git_secrets_hooks .install_pre_commit_hooks
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

_docs/index.md: notebooks/index.ipynb dist
	jupyter nbconvert --to markdown --stdout --RegexRemovePreprocessor.patterns="['\# hide', '\#hide']" notebooks/index.ipynb | sed "s/{{ get_airt_client_version }}/$$(pip show airt-client | grep Version | cut -d ":" -f 2 | xargs)/" > _docs/index.md
    
_docs/Tutorial.md: notebooks/Tutorial.ipynb dist
	jupyter nbconvert --to markdown --stdout --RegexRemovePreprocessor.patterns="['\# hide', '\#hide']" notebooks/Tutorial.ipynb > _docs/Tutorial.md

_docs/SUMMARY.md: generate_summary.ipynb dist
	jupyter nbconvert --execute --stdout --to markdown generate_summary.ipynb > /dev/null

_docs/API/cli: generate_cli_doc.ipynb _docs/SUMMARY.md dist
	jupyter nbconvert --execute --stdout --to markdown generate_cli_doc.ipynb > /dev/null
	touch _docs/API/cli

README.md: _docs/index.md
	cp _docs/index.md README.md

_docs/RELEASE.md:
	cp RELEASE.md _docs/

_docs/rest_api_docs.md: rest_api_docs.md
	cp rest_api_docs.md _docs/

site: dist README.md _docs/index.md _docs/Tutorial.md _docs/SUMMARY.md \
      _docs/RELEASE.md _docs/rest_api_docs.md mkdocs.yml \
      _docs/API/cli
	mkdocs build
	touch site

docs_serve: site
	python -m http.server 6007 --bind 0.0.0.0 --directory ./site/
#	mkdocs serve -a 0.0.0.0:6007

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
	rm -rf _docs/Tutorial.md _docs/index.md _docs/SUMMARY.md _docs/RELEASE.md _docs/rest_api_docs.md _docs/API
	rm -rf site
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
