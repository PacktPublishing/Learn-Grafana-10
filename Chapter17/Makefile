
build:
	docker-compose pull grafana

up:
	docker-compose up --pull missing -d grafana

down:
	docker-compose down

start:
	docker-compose start grafana

stop:
	docker-compose stop grafana

restart:
	docker-compose restart grafana

clean:
	docker-compose rm -vs

auto: build up down