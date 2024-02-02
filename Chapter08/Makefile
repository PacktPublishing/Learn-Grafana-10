CHAPTER=ch8
IMAGE=python
TAG=$(IMAGE)/$(CHAPTER)

APPPATH=/usr/src/app
APP=earthquake.py
TEMPFILE=/data/eq.txt

EQ_SIZE=all
EQ_WINDOW=week
EQ_PRECISION=ms

INFLUX_URL=http://influxdb:8086
INFLUX_ORG=LearnGrafana
INFLUX_BUCKET=Chapter08
#INFLUX_API_TOKEN=

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

build-earthquake:
	docker build --pull --tag $(TAG) .

help-earthquake:
	docker run --rm \
		-v "$$(PWD)/app:/usr/src/app" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/$(APP) --help

dump-earthquake:
	docker run --rm \
		-v "$$(PWD)/app:/usr/src/app" \
		-v "$$(PWD)/data:/data" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/$(APP) \
		--size $(EQ_SIZE) \
		--window $(EQ_WINDOW) \
		--output $(TEMPFILE)

load-earthquake:
	docker run --rm --network=host \
		-v "$$(PWD)/app:/usr/src/app" \
		-v "$$(PWD)/data:/data" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/$(APP) \
		--input $(TEMPFILE) \
		--precision $(EQ_PRECISION) \
		--db $(INFLUX_BUCKET) \
		--token=$(INFLUX_API_TOKEN)

reload-earthquake: dump-earthquake load-earthquake
full-reload-earthquake: build-earthquake reload-earthquake

test-influxdb:
	curl -i http://localhost:8086/ping

auto: build up test-influxdb build-$(IMAGE) full-load-earthquake
