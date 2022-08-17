# with docker
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker run --name charts \
    --restart always \
    -v $(pwd)/default.conf:/etc/nginx/conf.d/default.conf \
    -v $(pwd)/images/:/root/ \
    -p 80:80 \
    -d nginx