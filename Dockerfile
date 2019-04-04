FROM python:3.6
LABEL maintainer "Marius Stanca <me@marius.xyz>"


# Fix locale
RUN echo "LC_ALL=en_US.UTF-8" > /etc/default/locale && \
    echo "LANG=en_US.UTF-8" >> /etc/default/locale

# Add executable
ADD dist/trequire.pex /bin/trequire

ENTRYPOINT ["/bin/trequire"]
