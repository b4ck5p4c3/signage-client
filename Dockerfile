FROM alpine:3.16
RUN apk --no-cache add python3 py3-beautifulsoup4 py3-unidecode py3-paho-mqtt \
	py3-requests
COPY ./src /opt/signage-client
ENTRYPOINT [ "/opt/signage-client/baneks.py" ]
