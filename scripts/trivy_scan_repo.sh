#!/bin/bash


if [[ -n ${CI} ]]; then # ${CI} is available for all jobs executed in CI/CD. true when available.
    cmd="trivy fs --security-checks vuln,config,secret \
    --exit-code 1 \
    --skip-files ./allowed_secrets.txt \
    ./"
    (set -x; ${cmd})
else  
    cmd="trivy fs --security-checks vuln,config,secret \
    --exit-code 1 \
    --skip-files ./.env.dev.secrets \
    --skip-files ./allowed_secrets.txt \
    ./"
    (set -x; ${cmd})
fi
