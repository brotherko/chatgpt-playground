FROM alpine
ENV VERSION 1.11.0
RUN apk add --no-cache tinyproxy
COPY tinyproxy.conf /etc/tinyproxy/tinyproxy.conf
EXPOSE 8888
CMD ["tinyproxy", "-d"]