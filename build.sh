#! /bin/sh

if [ $# -ne 1 ]; then
	echo "Argument missing [ build | refresh | logs ]"
		exit 1
fi


if [ $1 = "build" ]; then
        git pull && docker build . --tag screenless-server:latest && docker-compose down && docker-compose up -d && docker-compose logs -f;
                exit 0
elif [ $1 = "refresh" ]; then
	docker build . --tag screenless-server:latest && docker-compose down && docker-compose up -d && docker-compose logs -f;
		exit 0
elif [ $1 = "logs" ]; then
        docker-compose logs -f;
		exit 0
fi

