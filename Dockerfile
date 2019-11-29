FROM amazonlinux:latest
COPY pin-yum-repos.py /root
RUN /root/pin-yum-repos.py
RUN yum update -y; yum clean all
# re-run just in case repo config would have been updated, usually no-op
RUN /root/pin-yum-repos.py
