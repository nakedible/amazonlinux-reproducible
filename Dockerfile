FROM amazonlinux:latest
COPY pin-yum-repos.py /root
RUN /root/pin-yum-repos.py && yum update -y && yum clean all && /root/pin-yum-repos.py
