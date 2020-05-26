FROM registry.redhat.io/rhel8/python-38
LABEL authors="Aberson Malivert(amaliver@redhat.com),Ashley Kim(akim@redhat.com, Julia Walker(juwalker@redhat.com), Pablo Castillo(pcastill@redhat.com), Sarah Zhong(szhong@redhat.com)
USER root 
RUN dnf install -y python3-pip
RUN cd /usr/local/bin/
RUN git clone https://github.com/amalivert/certification_notifier.git
RUN cd /usr/local/bin/certification_notifier/
RUN git checkout dev
RUN python3 -m pip install -r requirements.txt
CMD [ "python3", "./rh_cert_notify.py"]


