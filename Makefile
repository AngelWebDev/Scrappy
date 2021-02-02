build:
	docker-compose build app

yarn:
	docker run -v ${PWD}:/app node:latest sh -c "cd /app && yarn install"

push:
	docker push 100days/scrappy

start:
	docker-compose up

stop:
	docker-compose --remove-orphans --volumes down
