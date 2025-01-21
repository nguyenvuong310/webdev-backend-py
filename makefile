
build:
	docker buildx build --platform linux/amd64 -t vuong676/gscore:latest .

push:
	docker push vuong676/gscore:latest

conatainer-up:
	docker-compose up -d

container-down:
	docker-compose down

up: 
	python3 manage.py runserver 

install:
	pip3 install -r requirements.txt

migrate:
	python3 manage.py migrate

