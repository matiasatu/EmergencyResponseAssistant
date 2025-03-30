docker stop frontend && docker rm frontend
docker build -t frontend .
docker run -p 8001:5173 --rm --name frontend frontend
