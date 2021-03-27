#!/bin/bash
app="my_docker_image"
docker build -t ${app} .
docker run -d -p 5000:5000 \
  --network=host \
  --name=${app} \
  -v $PWD:/app ${app}
