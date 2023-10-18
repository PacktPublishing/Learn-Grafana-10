CHAPTER=ch5
IMAGE=python
TAG=$(IMAGE)/$(CHAPTER)

APP=weather.py
TEMPFILE=wx.txt
STATIONS=KSFO,KDEN,KSTL,KJFK

INFLUX_URL=http://influxdb:8086
INFLUX_ORG=LearnGrafana
INFLUX_BUCKET=chapter05
INFLUX_API_TOKEN=eXYHDXnvzQ8NAjI0ARDjlW9k7bEAx3v1O8kaxuLfFWvJ0SXf0b47yMCWJIt8o7NPtmJOJSIWuNh9JZ3PrOugEw==


pull:
	docker-compose pull

up:
	docker-compose up -d --pull missing

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop

influxdb-bucket-create:
	docker-compose exec -T \
    	influxdb influx bucket create  \
        --org $(INFLUX_ORG) \
        --token $(INFLUX_API_TOKEN) \
		--name $(INFLUX_BUCKET)

influxdb-bucket-delete:
	docker-compose exec -T \
    	influxdb influx bucket delete  \
        --org $(INFLUX_ORG) \
        --token $(INFLUX_API_TOKEN) \
		--name $(INFLUX_BUCKET)

influxdb-bucket-refresh: influxdb-bucket-delete influxdb-bucket-create

build-weather:
	docker build --pull --tag $(TAG) .

dump-weather:
	docker run --rm \
		$(TAG) $(APP) \
		--output $(TEMPFILE) \
		--stations $(STATIONS)

load-weather:
	docker run --rm --network=host \
		-v "$$(PWD):/usr/src/app" \
		$(TAG) $(APP) \
 		--input $(TEMPFILE) \
		--db $(INFLUX_BUCKET) --token $(INFLUX_API_TOKEN)

reload-weather: dump-weather load-weather

full-reload-weather: build-weather reload-weather

test-influxdb:
	curl -i http://localhost:8086/ping

auto: pull up test-influxdb influxdb-bucket-refresh full-reload
