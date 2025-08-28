

cache:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf


docker_deploy:
	docker rm -f etl_instance 
	docker build -t etl_api  .	--no-cache
	docker run   -it --restart=always -d -p 8206:8000 --name etl_instance etl_api

docker_build:
	docker build -t etl  .	

docker_exec:
	docker exec -it conservare /bin/bash /bin/bash

docker_rm:
	docker rm -f etl_instance 

poetry_update:
	poetry env activate
	poetry update

 - ssl_registry:
  - sudo certbot certonly --standalone -d etlapidev.iocasta.com.br

