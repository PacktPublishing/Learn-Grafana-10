IMAGE=python
TAG=$(IMAGE)/ch8

WX_BIN=bin/weather.py
WX_BUCKET=weatherdb
WX_TEMPFILE=data/wx.txt
WX_STATIONS=KSFO,KDEN,KSTL,KJFK

EQ_BIN=bin/earthquake.py
EQ_BUCKET=Chapter08
EQ_TEMPFILE=data/eq.txt
EQ_SIZE=all
EQ_WINDOW=week
EQ_PRECISION=ms

INFLUX_URL=http://influxdb:8086
INFLUX_ORG=LearnGrafana
INFLUX_API_TOKEN=***REMOVED***

pull:
	docker-compose pull

up:
	docker-compose up -d

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

bucket-refresh-earthquake: bucket-delete-bucket bucket-create-earthquake 

dump-earthquake:
	docker run --rm --network=host -v "$$(PWD):/usr/src/app" \
		--name $(IMAGE) $(TAG) \
		earthquake.py \
		--size $(EQ_SIZE) \
		--window $(EQ_WINDOW) \
		--output $(EQ_TEMPFILE)

load-earthquake:
	docker run --rm --network=host -v "$$(PWD):/usr/src/app" \
		--name $(IMAGE) $(TAG) \
		earthquake.py \
		--token=$(INFLUX_API_TOKEN) \
		--input $(EQ_TEMPFILE) \
		--precision $(EQ_PRECISION) \
		--db $(EQ_BUCKET)


reload-earthquake: dump-earthquake load-earthquake
full-load-earthquake: bucket-refresh-earthquake reload-earthquake

test-influxdb:
	curl -i http://localhost:8086/ping

auto: build up test-influxdb build-$(IMAGE) full-load-weather full-load-earthquake
