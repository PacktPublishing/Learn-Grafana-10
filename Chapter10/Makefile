SMALL=100
MEDIUM=1000
LARGE=10000

DATADIR=data
CSVFILE=$(DATADIR)/Current_FY_Cases.csv
INDEX=data-index

PASS=tcL1ZZ*eWYSDe8s_PpE4

pull:
	docker-compose pull

up: up-grafana up-elasticsearch

up-%:
	docker-compose up --pull missing -d $*

down:
	docker-compose down

start:
	docker-compose start

stop:
	docker-compose stop

build-$(IMAGE):
	docker build --pull --tag $(TAG) .

$(CSVFILE):
	gunzip $(CSVFILE).gz

load-es-small: clean-es
	head -$(SMALL) $(CSVFILE) | docker-compose run -T logstash logstash

load-es-medium: clean-es
	head -$(MEDIUM) $(CSVFILE) | docker-compose run -T logstash logstash

load-es-large: clean-es
	head -$(LARGE) $(CSVFILE) | docker-compose run -T logstash logstash

load-es-full: clean-es
	cat $(CSVFILE) | docker-compose run -T logstash logstash

describe-es:
	curl -XGET http://localhost:9200/$(INDEX)/_mapping?pretty

query-es:
	curl -XGET http://localhost:9200/$(INDEX)/_search?pretty

clean-es:
	curl -X DELETE "localhost:9200/$(INDEX)?pretty"

test-es:
	curl -XGET http://localhost:9200

auto: up $(CSVFILE) load-es-all