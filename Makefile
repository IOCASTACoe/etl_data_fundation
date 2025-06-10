

cache:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

docker_build:
	docker build -t etl  .	

docker_run:
	docker run -it -d -p 7500:80 --restart=always --name etl_instance etl

docker_exec:
	docker exec -it conservare /bin/bash /bin/bash

docker_rm:
	docker rm -f etl_instance etl

poetry_update:
	poetry env activate
	oetry update

