build:
	docker build . --platform=linux/amd64 -t chatgpt_playground_server

run:
	docker run --env-file .env --platform linux/amd64 -p 5000:80 chatgpt_playground_server

dev:
	poetry run dev