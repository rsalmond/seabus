FROM debian:latest
RUN apt-get update && apt install git g++ make cmake automake libtool pkg-config \
	libusb-1.0-0-dev libfftw3-dev librtlsdr-dev -y && \
	git clone https://github.com/steve-m/kalibrate-rtl.git /kalibrate && \
	cd /kalibrate && ./bootstrap && ./configure CXXFLAGS='-W -Wall -O3' && \
	make

FROM debian:latest
RUN apt-get update && apt install libfftw3-3 librtlsdr0 -y && apt-get clean && apt-get autoclean
COPY --from=0 /kalibrate/src/kal /usr/local/bin
