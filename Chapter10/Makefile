SMALL=100
MEDIUM=1000
LARGE=10000
XLARGE=100000
XXLARGE=1000000

DATADIR=data
CSVFILE=Current_FY_Cases.csv
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
	gunzip $(DATADIR)/$(CSVFILE).gz

make-subsets: make-es-small make-es-medium make-es-large

make-es-small:
	tail -$(SMALL) $(DATADIR)/$(CSVFILE) > $(DATADIR)/$(basename $(CSVFILE))-small.csv

load-es-small: clean-es
	tail -$(SMALL) $(DATADIR)/$(CSVFILE) | docker-compose run -T logstash logstash

make-es-medium:
	tail -$(MEDIUM) $(DATADIR)/$(CSVFILE) > $(DATADIR)/$(basename $(CSVFILE))-medium.csv

load-es-medium: clean-es
	tail -$(MEDIUM) $(DATADIR)/$(CSVFILE) | docker-compose run -T logstash logstash

make-es-large:
	tail -$(LARGE) $(DATADIR)/$(CSVFILE) > $(DATADIR)/$(basename $(CSVFILE))-large.csv

load-es-large: clean-es
	tail -$(LARGE) $(DATADIR)/$(CSVFILE) | docker-compose run -T logstash logstash

make-es-xlarge:
	tail -$(XLARGE) $(DATADIR)/$(CSVFILE) > $(DATADIR)/$(basename $(CSVFILE))-xlarge.csv

load-es-xxlarge: clean-es
	tail -$(XLARGE) $(DATADIR)/$(CSVFILE) | docker-compose run -T logstash logstash

make-es-xxlarge:
	tail -$(XXLARGE) $(DATADIR)/$(CSVFILE) > $(DATADIR)/$(basename $(CSVFILE))-xxlarge.csv

load-es-xxlarge: clean-es
	tail -$(XXLARGE) $(DATADIR)/$(CSVFILE) | docker-compose run -T logstash logstash

load-es-full: clean-es
	cat $(DATADIR)/$(CSVFILE) | docker-compose run -T logstash logstash

describe-es:
	curl -XGET http://localhost:9200/$(INDEX)/_mapping?pretty

query-es:
	curl -XGET http://localhost:9200/$(INDEX)/_search?pretty

clean-es:
	curl -X DELETE "localhost:9200/$(INDEX)?pretty"

test-es:
	curl -XGET http://localhost:9200

auto: up $(CSVFILE) load-es-all