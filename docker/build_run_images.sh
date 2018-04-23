#! /bin/sh

cd "$(dirname $0)"

curl -L https://download.docker.com/linux/static/stable/x86_64/docker-18.03.0-ce.tgz | tar xvzf - docker/docker
mv docker/docker docker-bin
rm -rf docker

for v in "3.7-rc-alpine" "3.6-alpine" "3.5-alpine" "3.4-alpine" "2-alpine3.7"; do
  echo "travis_fold:start:$v"
  echo "FROM python:$v" > Dockerfile.tmp
  cat Dockerfile >> Dockerfile.tmp
  docker build -t "vunit/run:$v" -f Dockerfile.tmp .
  echo "travis_fold:end:$v"
done

rm -rf docker-bin Dockerfile.tmp

docker images
