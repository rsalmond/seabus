FROM debian:latest
RUN apt-get update && apt install git g++ make pkg-config \
	libusb-1.0-0-dev librtlsdr-dev -y && \
	git clone https://github.com/dgiardini/rtl-ais.git /rtl-ais && \
	cd /rtl-ais && make

FROM debian:latest
RUN apt-get update && apt install librtlsdr0 -y && apt-get clean && apt-get autoclean
COPY --from=0 /rtl-ais/rtl_ais /usr/local/bin
