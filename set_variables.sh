#!/bin/bash

export AIRT_CLIENT_DOCKER=ghcr.io/airtai/airt-service-dev:latest

BRANCH=$(git branch --show-current)
if [ "$BRANCH" == "main" ]; then
    TAG=latest
elif [ "$BRANCH" == "dev" ]; then
    TAG=dev
else
    if [ "$(docker image ls -q $AIRT_CLIENT_DOCKER:$BRANCH)" == "" ]; then
        TAG=dev
    else
        TAG=$BRANCH
    fi
fi

if [ "$BRANCH" == "main" ]; then
    AIRT_SERVICE_FILE_BRANCH=main
else
    AIRT_SERVICE_FILE_BRANCH=dev
fi

export TAG BRANCH AIRT_SERVICE_FILE_BRANCH

if test -z "$AIRT_JUPYTER_PORT"; then
      echo 'AIRT_JUPYTER_PORT variable not set, setting to 8888'
      export AIRT_JUPYTER_PORT=8888
else
    echo AIRT_JUPYTER_PORT variable set to $AIRT_JUPYTER_PORT
fi

if test -z "$AIRT_TB_PORT"; then
      echo 'AIRT_TB_PORT variable not set, setting to 6006'
      export AIRT_TB_PORT=6006
else
    echo AIRT_TB_PORT variable set to $AIRT_TB_PORT
fi

if test -z "$AIRT_DASK_PORT"; then
      echo 'AIRT_DASK_PORT variable not set, setting to 8787'
      export AIRT_DASK_PORT=8787
else
    echo AIRT_DASK_PORT variable set to $AIRT_DASK_PORT
fi

if test -z "$AIRT_DOCS_PORT"; then
      echo 'AIRT_DOCS_PORT variable not set, setting to 4000'
      export AIRT_DOCS_PORT=4000
else
      echo AIRT_DOCS_PORT variable set to $AIRT_DOCS_PORT
fi

if test -z "$AIRT_DATA"; then
      echo 'AIRT_DATA variable not set, setting to current directory'
      export AIRT_DATA=`pwd`
fi
echo AIRT_DATA variable set to $AIRT_DATA

if test -z "$AIRT_PROJECT"
then
      echo 'AIRT_PROJECT variable not set, setting to current directory'
      export AIRT_PROJECT=`pwd`
fi
echo AIRT_PROJECT variable set to $AIRT_PROJECT

if test -z "$AIRT_GPU_PARAMS"
then
      echo 'AIRT_GPU_PARAMS variable not set, setting to all GPU-s'
      export AIRT_GPU_PARAMS="--gpus all"
fi
echo AIRT_GPU_PARAMS variable set to $AIRT_GPU_PARAMS

echo Using $AIRT_CLIENT_DOCKER
docker image ls $AIRT_CLIENT_DOCKER


export UID=$(id -u)
export GID=$(id -g)


# Check .env.dev.* file exists and copy from template if it does not exists
if [ ! -f .env.dev.config ]; then
      cp .env.template.config .env.dev.config
fi

if [ ! -f .env.dev.secrets ]; then
      cp .env.template.secrets .env.dev.secrets
      echo 'Please update the environment variable values in file .env.dev.config, .env.dev.secrets and rerun the script'
      exit -1
fi


# Run envsubst for .env.dev.* files
cp .env.dev.config /tmp/airt-client.env.dev.config && envsubst < /tmp/airt-client.env.dev.config > .env.dev.config && rm /tmp/airt-client.env.dev.config
cp .env.dev.secrets /tmp/airt-client.env.dev.secrets && envsubst < /tmp/airt-client.env.dev.secrets > .env.dev.secrets && rm /tmp/airt-client.env.dev.secrets
# Export values in .env.dev.* files as environment variables for validation
set -a && source .env.dev.config && source .env.dev.secrets && set +a

if test -z "$AIRT_SERVICE_SUPER_USER_PASSWORD"
then
      echo 'AIRT_SERVICE_SUPER_USER_PASSWORD variable not set in .env.dev.secrets file, exiting'
      exit -1
fi

if test -z "$AIRT_TOKEN_SECRET_KEY"
then
      echo 'AIRT_TOKEN_SECRET_KEY variable not set in .env.dev.secrets file, exiting'
      exit -1
fi

if test -z "$AIRT_SERVICE_SUPER_USER"
then
      export AIRT_SERVICE_SUPER_USER="kumaran"
      echo 'AIRT_SERVICE_SUPER_USER variable not set, setting to default super user name'
fi

if test -z "$AIRT_SERVICE_USERNAME"
then
      export AIRT_SERVICE_USERNAME="johndoe"
      echo AIRT_SERVICE_USERNAME variable set to $AIRT_SERVICE_USERNAME
fi

if test -z "$AWS_ACCESS_KEY_ID"
then
      echo 'AWS_ACCESS_KEY_ID variable not set in .env.dev.secrets file, exiting'
      exit -1
fi

if test -z "$AWS_SECRET_ACCESS_KEY"
then
      echo 'AWS_SECRET_ACCESS_KEY variable not set in .env.dev.secrets file, exiting'
      exit -1
fi

if test -z "$STORAGE_BUCKET_PREFIX"
then
      echo 'STORAGE_BUCKET_PREFIX variable not set in .env.dev.secrets file, exiting'
      exit -1
fi

export AIRT_SERVER_DOCKER="ghcr.io/airtai/airt-service"
AIRT_SERVER_DOCKER=$AIRT_SERVER_DOCKER:$TAG

export AIRT_SERVICE_PORT="${PORT_PREFIX}6007"
echo AIRT_SERVICE_PORT variable set to $AIRT_SERVICE_PORT

export DOMAIN="${USER}-airt-service"
echo DOMAIN variable set to $DOMAIN

export DROP_MESSAGES="--drop-messages"
echo DROP_MESSAGES variable set to $DROP_MESSAGES

export DOCKER_COMPOSE_PROJECT="${USER}-airt-client"
echo DOCKER_COMPOSE_PROJECT variable set to $DOCKER_COMPOSE_PROJECT

export AIRT_SERVER_URL="http://airt-service:6006"
echo AIRT_SERVER_URL variable set to $AIRT_SERVER_URL

export AIRT_SERVER_GITLAB_ID=29120234
echo AIRT_SERVER_GITLAB_ID variable set to $AIRT_SERVER_GITLAB_ID

if test -z "$ACCESS_REP_TOKEN"
then
      echo 'ACCESS_REP_TOKEN variable not set in .env.dev.secrets file, exiting'
      exit -1
fi

export URI_ENCODED_FILE_PATH="docker%2Fdependencies%2Eyml"
echo URI_ENCODED_FILE_PATH variable set to $URI_ENCODED_FILE_PATH

export DOWNLOAD_FILE_DESTINATION="docker/dependencies.yml"
echo DOWNLOAD_FILE_DESTINATION variable set to $DOWNLOAD_FILE_DESTINATION

export PRESERVE_ENVS=$(cat .env.dev.* | cut -f1 -d"=" | sed '/^#/d' |  tr '\n' ',')
export PRESERVE_ENVS="${PRESERVE_ENVS}AIRT_SERVER_URL,AIRT_SERVICE_USERNAME,AIRT_SERVICE_PASSWORD,AIRT_SERVICE_SUPER_USER"
# echo $PRESERVE_ENVS
