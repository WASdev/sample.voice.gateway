FROM registry.access.redhat.com/ubi8/ubi:8.3
LABEL name="voice-call-monitor"

RUN yum update --disableplugin=subscription-manager -y \
    && yum install --disableplugin=subscription-manager gcc gcc-c++ ncurses-devel wget hostname make -y \
    && rm -rf /var/cache/yum

RUN mkdir /SIP; cd /SIP; wget "https://github.com/SIPp/sipp/releases/download/v3.5.1/sipp-3.5.1.tar.gz" \
	&& tar -xvzf sipp-3.5.1.tar.gz \
	&& cd /SIP/sipp-3.5.1; ./configure --with-rtpstream \
 	&& make

COPY src/* /src/
COPY src/sipp-files/* /SIP/sipp-3.5.1/

WORKDIR /src

RUN useradd -u 1001 -r -g 0 -s /sbin/nologin default \
    && mkdir -p /home/default \
    && chown -R 1001:0 /home/default \
    && chmod -R g+rw /home/default \
    && chown -R 1001:0 /src \
    && chmod -R g+rw /src \
    && chmod +x /src/*.sh \
    && chown -R 1001:0 /SIP \
    && chmod -R g+rw /SIP

USER 1001

ENTRYPOINT ["./voice-call-monitor.sh"]
