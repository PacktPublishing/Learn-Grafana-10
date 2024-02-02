APPS := grafana

build-%:
	docker-compose pull $*

up-%:
	docker-compose up --pull missing -d $*

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop


auto: build up-grafana

