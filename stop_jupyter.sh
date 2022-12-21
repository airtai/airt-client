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

docker-compose -p $DOCKER_COMPOSE_PROJECT -f $DOWNLOAD_FILE_DESTINATION -f docker/client.yml --profile dev down
