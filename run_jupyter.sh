#!/bin/bash

source set_variables.sh


if `which nvidia-smi`
then
	echo INFO: Running docker image with: $AIRT_GPU_PARAMS
	nvidia-smi -L
	export GPU_PARAMS=$AIRT_GPU_PARAMS
else
	echo INFO: Running docker image without GPU-s
	export GPU_PARAMS=""
fi

echo Trying to download file from "https://gitlab.com/api/v4/projects/$AIRT_SERVER_GITLAB_ID/repository/files/$URI_ENCODED_FILE_PATH/raw?ref=$AIRT_SERVICE_FILE_BRANCH"

curl -o $DOWNLOAD_FILE_DESTINATION --header "PRIVATE-TOKEN: $ACCESS_REP_TOKEN" "https://gitlab.com/api/v4/projects/$AIRT_SERVER_GITLAB_ID/repository/files/$URI_ENCODED_FILE_PATH/raw?ref=$AIRT_SERVICE_FILE_BRANCH"

echo Download Successful

	
docker-compose -p $DOCKER_COMPOSE_PROJECT -f $DOWNLOAD_FILE_DESTINATION -f docker/client.yml --profile dev up -d --no-recreate

sleep 10

docker logs $USER-airt-client 2>&1 | grep token
