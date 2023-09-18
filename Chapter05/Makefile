IMAGE=weather
TAG=$(IMAGE)/ch5
TEMPFILE=wx.txt
STATIONS=KSFO,KDEN,KSTL,KJFK

INFLUX_URL=http://influxdb:8086
INFLUX_ORG=LearnGrafana
INFLUX_BUCKET=chapter05
INFLUX_API_TOKEN=***REMOVED***


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

build-$(IMAGE):
	docker build --pull --tag $(TAG) .

dump-$(IMAGE):
	docker run --rm --network=host -v "$$(PWD):/usr/src/app" --name $(IMAGE) $(TAG) \
		--output $(TEMPFILE) --stations $(STATIONS)

load-$(IMAGE):
	docker run --rm --network=host -v "$$(PWD):/usr/src/app" --name $(IMAGE) $(TAG) \
 		--input $(TEMPFILE) --db $(INFLUX_BUCKET) --token $(INFLUX_API_TOKEN)

reload: dump-$(IMAGE) load-$(IMAGE)

full-reload: build-$(IMAGE) dump-$(IMAGE) load-$(IMAGE)

test-influxdb:
	curl -i http://localhost:8086/ping

auto: pull up test-influxdb influxdb-bucket-refresh full-reload
