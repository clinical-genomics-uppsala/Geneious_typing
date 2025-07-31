FROM --platform=linux/amd64 ncbi/blast:2.16.0

LABEL maintainer="ida.karlsson@scilifelab.uu.se"
LABEL spatyper=1.0.0
LABEL version=1.0.0

# Set workdir
WORKDIR /

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip \
    && apt-get clean \
    && apt-get purge \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/list/* \
    && pip install --no-cache-dir cgecore

RUN wget https://bitbucket.org/genomicepidemiology/spatyper/get/b5f57c094f9c4cc139b8ead0e471d385f23aa507.tar.gz \ 
    && mkdir spatyper \
    && tar -xf b5f57c094f9c4cc139b8ead0e471d385f23aa507.tar.gz -C spatyper --strip-components 1
