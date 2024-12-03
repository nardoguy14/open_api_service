#!/bin/bash

pwd
echo "yo"
export POSTGRES_HOST=$(aws rds describe-db-instances --db-instance-identifier nardos-db --query "DBInstances[0].Endpoint.Address")
export POSTGRES_HOST=$(echo ${POSTGRES_HOST//\"/})
export POSTGRES_DB=nardosdb
export POSTGRES_USER=nardo
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD # set by git actions to cloudformation to userdata in ec2

echo $POSTGRES_HOST
#
#export USING_FAST_API=1
#
#sudo docker network create my-network || true
#
#echo "stopping containers"
## Stop any existing container
#sudo docker stop open_ai_embeddings_service || true
#sudo docker rm open_ai_embeddings_service || true
#sudo docker stop embeddings_consumer || true
#sudo docker rm embeddings_consumer || true
#sudo docker stop datascrape_consumer || true
#sudo docker rm datascrape_consumer || true
#
#docker rmi $(docker images -q)
#
#
#echo "pulling latest image"
## Pull the latest image
#sudo docker pull nardoarevalo14/embeddings_consumer:latest
#sudo docker pull nardoarevalo14/datascrape_consumer:latest
#sudo docker pull nardoarevalo14/openai_embeddings_service:latest
#
#echo "running api container"
#sudo docker run -d --name open_ai_embeddings_service -p 80:8000 \
# -e POSTGRES_HOST=$POSTGRES_HOST \
# -e POSTGRES_DB=$POSTGRES_DB \
# -e POSTGRES_USER=$POSTGRES_USER \
# -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
# -e USING_FAST_API=$USING_FAST_API \
# -e MIVILUS_HOST=$MIVILUS_HOST \
# -e MIVILUS_PORT=$MIVILUS_PORT \
# --network my-network \
# nardoarevalo14/openai_embeddings_service:latest
#
#
#echo "running embeddings container"
#sudo docker run -d --name embeddings_consumer -p 8000:8000 \
#  -e POSTGRES_HOST=$POSTGRES_HOST \
#  -e POSTGRES_DB=$POSTGRES_DB \
#  -e POSTGRES_USER=$POSTGRES_USER \
#  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
#  -e USING_FAST_API=$USING_FAST_API \
#  -e MIVILUS_HOST=$MIVILUS_HOST \
#  -e MIVILUS_PORT=$MIVILUS_PORT \
# --network my-network \
# nardoarevalo14/embeddings_consumer:latest
#
#sleep 10
#
#echo "running datascraper container"
#sudo docker run -d --name datascrape_consumer \
# -e POSTGRES_HOST=$POSTGRES_HOST \
# -e POSTGRES_DB=$POSTGRES_DB \
# -e POSTGRES_USER=$POSTGRES_USER \
# -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
# -e USING_FAST_API=$USING_FAST_API \
# -e MIVILUS_HOST=$MIVILUS_HOST \
# -e MIVILUS_PORT=$MIVILUS_PORT \
# --network my-network \
# nardoarevalo14/datascrape_consumer:latest


sudo docker-compose -f /home/ec2-user/app/docker-compose-deploy.yml up -d
