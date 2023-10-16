CHAPTER=ch7
IMAGE=python
TAG=$(IMAGE)/$(CHAPTER)

APPPATH=/usr/src/app
APP=weather.py
TEMPFILE=/data/wx.txt
STATIONS=KSFO,KDEN,KSTL,KJFK

INFLUX_URL=http://influxdb:8086
INFLUX_ORG=LearnGrafana
INFLUX_BUCKET=Chapter07
INFLUX_API_TOKEN=XuWvVqWanFeaWSPHR-OTfagATO2IdYdt3xOE8nAcTNJGdhjSmXjofA8qhJYxRo7VMW_JMQozck1AeDERMgBQQw==

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

build-weather:
	docker build --pull --tag $(TAG) .

help-weather:
		docker run --rm \
		-v "$$(PWD)/app:/usr/src/app" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/weather.py --help

dump-weather:
		docker run --rm \
		-v "$$(PWD)/app:/usr/src/app" \
		-v "$$(PWD)/data:/data" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/weather.py \
		--output $(TEMPFILE) \
		--stations $(STATIONS)

load-weather:
	docker run --rm --network=host \
		-v "$$(PWD)/app:/usr/src/app" \
		-v "$$(PWD)/data:/data" \
		--name $(IMAGE)_$(CHAPTER) $(TAG) \
		$(APPPATH)/weather.py \
 		--input $(TEMPFILE) \
		--db $(INFLUX_BUCKET) --token $(INFLUX_API_TOKEN)

reload-weather: dump-weather load-weather

full-reload-weather: build-weather reload-weather

test-influxdb:
	curl -i http://localhost:8086/ping

auto: build up test-influxdb build-$(IMAGE) full-load-weather
