IMAGE=weather
TAG=$(IMAGE)/ch7

WX_BIN=weather.py
WX_TEMPFILE=data/wx.txt
WX_STATIONS=KSFO,KDEN,KSTL,KJFK

INFLUX_URL=http://influxdb:8086
INFLUX_ORG=LearnGrafana
INFLUX_BUCKET=Chapter07
INFLUX_API_TOKEN=9K_eE-rPS3AJQZ4Paieib1iJ0d7COuxRggbgqEG7hf4-at4bp4uLosWBINq7aeJbUpA8EhGqV3NS58ebES5lGQ==

INFLUX_URL=http://influxdb:8086
INFLUX_ORG=LearnGrafana
INFLUX_API_TOKEN=7dnOn5arpvJL-rEjnnMQ_KlQqXU73HYx9MxD_wXBEZYnu7-OocEOmAzU5xy6gcZOxeNwstp-wsZxytO3xKymVw==

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

bucket-create-weather:
	docker-compose exec -T \
    	influxdb influx bucket create  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(INFLUX_BUCKET)

bucket-delete-weather:
	docker-compose exec -T \
    	influxdb influx bucket delete  \
        --org $(INFLUX_ORG) \
        --token=$(INFLUX_API_TOKEN) \
		--name $(INFLUX_BUCKET)

bucket-refresh-weather: bucket-delete-weather bucket-create-weather 

dump-weather:
	docker run --rm --network=host -v "$$(PWD):/usr/src/app" \
		--name $(IMAGE) $(TAG) \
		$(WX_BIN) \
		--output $(WX_TEMPFILE) \
		--stations $(WX_STATIONS)

load-weather:
	docker run --rm --network=host -v "$$(PWD):/usr/src/app" \
		--name $(IMAGE) $(TAG) \
		$(WX_BIN) \
 		--token=$(INFLUX_API_TOKEN) \
		--input $(WX_TEMPFILE) \
		--db $(INFLUX_BUCKET)


reload-weather: dump-weather load-weather
full-reload-weather: weather-bucket-refresh reload-weather

test-influxdb:
	curl -i http://localhost:8086/ping

auto: build up test-influxdb build-$(IMAGE) full-load-weather
