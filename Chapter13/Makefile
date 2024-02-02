APPS := grafana loki promtail prometheus flog

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

test-loki:
	curl -XGET http://localhost:3100/ready

test-promtail:
	curl -XGET http://localhost:9080/ready

docker-plugin:
	docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
	docker plugin ls

auto: build up-grafana up-promtail up-loki test-promtail test-loki up-prometheus down

