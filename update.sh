#! /bin/sh
git pull && docker build . --tag screenless-server:latest && docker-compose down && docker-compose up -d && docker-compose logs -f;
