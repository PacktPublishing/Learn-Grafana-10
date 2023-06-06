IMAGE=python
TAG=$(IMAGE):ch9
TZ="America/Los Angeles"

PY_SERVICE=python

WX_BIN=bin/weather.py
WX_BUCKET=weatherdb
WX_TEMPFILE=data/wx.txt
WX_STATIONS=KSFO,KDEN,KSTL,KJFK

EQ_BIN=bin/earthquake.py
EQ_BUCKET=earthquakedb
EQ_TEMPFILE=data/eq.txt
EQ_SIZE=all
EQ_WINDOW=week
EQ_PRECISION=ms

INFLUX_HOST=influxdb
INFLUX_PORT=8086
INFLUX_URL=http://$(INFLUX_HOST):$(INFLUX_PORT)
INFLUX_ORG=LearnGrafana
INFLUX_API_TOKEN=kPL775NB1mn6n7T5kfLSXBNEe9Dy8v6f4fNS1Xvf8B7RgUeKdwG0jaw3uipxyWI5iW3C8WHvuPHsmA6y7AAhzQ==

pull:
	docker-compose pull

up:
	docker-compose up --pull missing -d

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop

build-$(IMAGE):
	docker build --pull --tag $(TAG) .

bucket-create-earthquake:
	docker-compose exec -T \
    	influxdb influx bucket create  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(EQ_BUCKET)

bucket-delete-earthquake:
	docker-compose exec -T \
    	influxdb influx bucket delete  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(EQ_BUCKET)

bucket-refresh-earthquake: bucket-delete-earthquake bucket-create-earthquake 

bucket-create-weather:
	docker-compose exec -T influxdb \
		influx bucket create  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(WX_BUCKET)

bucket-delete-weather:
	docker-compose exec -T influxdb \
		influx bucket delete  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(WX_BUCKET)

bucket-refresh-weather: bucket-delete-weather bucket-create-weather 

dump-earthquake:
	docker-compose run --rm \
		--name $(IMAGE) $(PY_SERVICE) \
		$(EQ_BIN) \
		--size $(EQ_SIZE) \
		--window $(EQ_WINDOW) \
		--output $(EQ_TEMPFILE)

load-earthquake:
	docker-compose run --rm \
		--name $(IMAGE) $(PY_SERVICE) \
		$(EQ_BIN) \
		--host=$(INFLUX_HOST) \
		--token=$(INFLUX_API_TOKEN) \
		--input $(EQ_TEMPFILE) \
		--precision $(EQ_PRECISION) \
		--db $(EQ_BUCKET)

reload-earthquake: dump-earthquake load-earthquake
full-load-earthquake: bucket-refresh-earthquake reload-earthquake

dump-weather:
	docker-compose run --rm \
		--name $(IMAGE) $(PY_SERVICE) \
		$(WX_BIN) \
		--output $(WX_TEMPFILE) \
		--stations $(WX_STATIONS)

load-weather:
	docker-compose run --rm \
		--name $(IMAGE) $(PY_SERVICE) \
		$(WX_BIN) \
		--host=$(INFLUX_HOST) \
 		--token=$(INFLUX_API_TOKEN) \
		--input $(WX_TEMPFILE) \
		--db $(WX_BUCKET)

reload-weather: dump-weather load-weather
full-reload-weather: bucket-refresh-weather reload-weather

test-influxdb:
	curl -i http://localhost:8086/ping

auto: build up test-influxdb build-$(IMAGE) full-load-weather full-load-earthquake
