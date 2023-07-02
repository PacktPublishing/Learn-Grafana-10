IMAGE=python
PY_SERVICE=python

MQTT_BIN=bin/mqtt_pub.py
BROKER=mosquitto
TOPIC="thermostat/mqtt"
INTERVAL=5
INPUT="data/thermostat_events.csv"

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

dump-events:
	docker-compose run --rm \
		--name $(IMAGE) $(PY_SERVICE) \
		$(MQTT_BIN) \
		--broker $(BROKER) \
		--topic $(TOPIC) \
		--input $(INPUT) \
		--interval $(INTERVAL)
