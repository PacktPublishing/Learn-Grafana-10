IMAGE=python
PY_SERVICE=python

INFLUX_ORG=LearnGrafana
CH12_BUCKET=Chapter12
#INFLUX_API_TOKEN=

up-%:
	docker-compose up --pull missing -d $*

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop

build-$(IMAGE):
	docker-compose build --pull python

bucket-create-chapter12:
	docker-compose exec -T influxdb \
		influx bucket create  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(CH12_BUCKET)

bucket-delete-chapter12:
	docker-compose exec -T influxdb \
		influx bucket delete  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(CH12_BUCKET)

bucket-refresh-chapter12: bucket-delete-chapter12 bucket-create-chapter12 
