docker-build:
	docker build . --platform=linux/amd64 -t gptpg_server

docker-run:
	docker run --env-file .env --platform linux/amd64 -p 4000:80 gptpg_server

dev:
	poetry run dev