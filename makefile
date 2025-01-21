
build:
	docker buildx build --platform linux/amd64 -t vuong676/gscore:latest .

push:
	docker push vuong676/gscore:latest

production:
	docker-compose -f docker-compose-production.yml up -d

up: 
	npm run start:dev

bootstrap:
	npm install --force or --legacy-peer-deps
	docker compose up -d
	npm run start:dev

