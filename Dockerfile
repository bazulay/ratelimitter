FROM fedora:29

MAINTAINER bazulay@gmail.com

RUN dnf update -y && dnf install -y supervisor psmisc && dnf clean all

#adding rluser  user & group to avoid running as root
RUN groupadd -g 1234 rluser && useradd -r -u 1234 -g 1234 -m  rluser

#Declaring the workdir
WORKDIR /opt/ratelimitter

#Adding the application files to the image , and creating necessary directories
ADD src/  /opt/ratelimitter
RUN mkdir /opt/ratelimitter/logs /opt/ratelimitter/run

#Chowning all files we have added  before switching to appuser
RUN chown -R rluser:rluser /opt/ratelimitter

USER rluser

#installing all necessary python packages
RUN pip3 install --user redis grpcio grpcio-tools


EXPOSE 46001

CMD /usr/bin/supervisord -n  -c /opt/ratelimitter/etc/supervisord.conf