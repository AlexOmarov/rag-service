FROM nvidia/cuda:12.5.1-cudnn-devel-ubuntu20.04

# Since wget is missing
RUN apt-get update && apt-get --no-install-recommends -y install wget && apt-get clean

#Install MINICONDA
RUN wget --secure-protocol=TLSv1_2 --max-redirect=0 https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh && \
	/bin/bash Miniconda.sh -b -p /opt/conda && \
	rm Miniconda.sh

ENV PATH=/opt/conda/bin:$PATH

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1 && apt-get clean

# Install gcc as it is missing in our base layer
RUN apt-get update && apt-get --no-install-recommends -y install gcc && apt-get clean

#  Create conda env
RUN conda config --set unsatisfiable_hints false

EXPOSE 5000

WORKDIR /berte-ai-service

ADD ./src/main /berte-ai-service/src/main
ADD environment.yaml /berte-ai-service/environment.yaml
ADD pyproject.toml /berte-ai-service/pyproject.toml

RUN conda env create -f environment.yaml

RUN useradd -ms /bin/bash docker
USER docker

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "berte-ai-service", "/bin/bash", "-c"]

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "-n", "berte-ai-service", "python", "src/main/app/app.py"]