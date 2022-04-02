# 基于python3.6镜像来构建owllook镜像
FROM python:3.6-slim-buster
MAINTAINER maolei133 <maolei133@163.com>

ADD . /owllook
WORKDIR /owllook

RUN pip install --no-cache-dir --upgrade pip ;\
    pip install --no-cache-dir pipenv ;\
    pipenv install --skip-lock ;\
    pipenv install --skip-lock ;\
    find . -name "*.pyc" -delete ;\
    rm -rf /var/cache/apk/* /tmp/*

EXPOSE 8001
