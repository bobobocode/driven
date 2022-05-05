ARG centos_version=7
FROM centos:$centos_version as builder
# needed to do again after FROM due to docker limitation
ARG centos_version

ARG nginx_version

# install dependencies
run yum install -y gcc gcc-c++\
    make \
    openssl-devel \
    pcre-devel \
    zlib-devel \
    python3-devel \
    python3 \
    wget \
    && yum clean all
