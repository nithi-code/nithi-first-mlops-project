# Base Jenkins LTS
FROM jenkins/jenkins:lts

USER root
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies + Docker CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        curl \
        git \
        docker.io \
        unzip \
    && rm -rf /var/lib/apt/lists/*

# Install docker-compose v2 (binary)
# RUN curl -L "https://github.com/docker/compose/releases/download/v2.23.1/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose && \
#    chmod +x /usr/local/bin/docker-compose

# Create Python venv
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip

ENV PATH="/opt/venv/bin:$PATH"

# Add Jenkins user to Docker group
ARG DOCKER_GID=999
RUN groupadd -g $DOCKER_GID docker || true && \
    usermod -aG docker jenkins && \
    mkdir -p /var/jenkins_home && chown -R jenkins:jenkins /var/jenkins_home

USER jenkins
WORKDIR /var/jenkins_home

EXPOSE 8080 50000

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/local/bin/jenkins.sh"]
