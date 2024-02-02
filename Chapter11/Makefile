IMAGE=python
PY_SERVICE=python

APPPATH=/usr/src/app
APP=mqtt_pub.py
BROKER=mosquitto
TOPIC="thermostat/mqtt"
INTERVAL=5
INPUT="/data/thermostat_events.csv"

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

help-events:
	docker-compose run --rm \
		--name $(IMAGE) $(PY_SERVICE) \
		$(APPPATH)/$(APP) \
		--help

dump-events:
	docker-compose run --rm \
		--name $(IMAGE) $(PY_SERVICE) \
		$(APPPATH)/$(APP) \
		--broker $(BROKER) \
		--topic $(TOPIC) \
		--input $(INPUT) \
		--interval $(INTERVAL)
