CHAPTER=ch9
IMAGE=python
TAG=$(IMAGE)/$(CHAPTER)

PY_SERVICE=python
APPPATH=/usr/src/app

WX_APP=weather.py
WX_BUCKET=weatherdb
WX_TEMPFILE=/data/wx.txt
WX_STATIONS=KSFO,KDEN,KSTL,KJFK

EQ_APP=earthquake.py
EQ_BUCKET=earthquakedb
EQ_TEMPFILE=/data/eq.txt
EQ_SIZE=all
EQ_WINDOW=week
EQ_PRECISION=ms

INFLUX_HOST=influxdb
INFLUX_PORT=8086
INFLUX_URL=http://$(INFLUX_HOST):$(INFLUX_PORT)
INFLUX_ORG=LearnGrafana
INFLUX_API_TOKEN=

pull:
	docker-compose pull --ignore-buildable

up:
	docker-compose up --pull missing -d grafana influxdb

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop

compose-build-$(IMAGE):
	docker-compose build $(IMAGE)

docker-build-$(IMAGE):
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
	docker-compose exec -T \
    	influxdb influx bucket create  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(WX_BUCKET)

bucket-delete-weather:
	docker-compose exec -T \
    	influxdb influx bucket delete  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(WX_BUCKET)

bucket-refresh-weather: bucket-delete-weather bucket-create-weather 

help-earthquake:
	docker run --rm \
		-v "$$(PWD)/app:/usr/src/app" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/$(EQ_APP) --help

dump-earthquake:
	docker-compose run $(PY_SERVICE) \
		$(APPPATH)/$(EQ_APP) \
		--size $(EQ_SIZE) \
		--window $(EQ_WINDOW) \
		--output $(EQ_TEMPFILE)

load-earthquake:
	docker-compose run $(PY_SERVICE) \
		$(APPPATH)/$(EQ_APP) \
		--host=$(INFLUX_HOST) \
		--input $(EQ_TEMPFILE) \
		--precision $(EQ_PRECISION) \
		--db $(EQ_BUCKET) \
		--token=$(INFLUX_API_TOKEN)

reload-earthquake: dump-earthquake load-earthquake
full-reload-earthquake: build-earthquake reload-earthquake

help-weather:
	docker run --rm \
		-v "$$(PWD)/app:/usr/src/app" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/$(WX_APP) --help

dump-weather:
	docker run --rm \
		-v "$$(PWD)/app:/usr/src/app" \
		-v "$$(PWD)/data:/data" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/$(WX_APP) \
		--output $(WX_TEMPFILE) \
		--stations $(WX_STATIONS)

load-weather:
	docker run --rm --network=host \
		-v "$$(PWD)/app:/usr/src/app" \
		-v "$$(PWD)/data:/data" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/$(WX_APP) \
 		--input $(WX_TEMPFILE) \
		--db $(WX_BUCKET) \
		--token=$(INFLUX_API_TOKEN)

reload-weather: dump-weather load-weather
full-reload-weather: build-weather reload-weather

test-influxdb:
	curl -i http://localhost:8086/ping

auto: build up test-influxdb build-$(IMAGE) full-load-weather full-load-earthquake
