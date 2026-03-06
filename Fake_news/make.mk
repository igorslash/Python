.PHONY: build run stop clean tensorboard

build:
	docker-compose build

run:
	docker-compose up training

run-detached:
	docker-compose up -d training

stop:
	docker-compose down

clean:
	docker-compose down -v
	docker system prune -f

tensorboard:
	docker-compose up tensorboard

logs:
	docker-compose logs -f training

shell:
	docker-compose run --rm training bash