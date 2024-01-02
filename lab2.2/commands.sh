docker build -t lab01_dd .
docker run -d -p 8016:80 -v /content/index.html:/usr/share/nginx/html/index.html lab01_dd
