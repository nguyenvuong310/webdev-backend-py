
build:
	docker buildx build --platform linux/amd64 -t vuong676/gscore:latest .

push:
	docker push vuong676/gscore:latest

production:
	docker-compose -f docker-compose-production.yml up -d

up: 
	python3 manage.py runserver 

install:
	pip install -r requirements.txt

