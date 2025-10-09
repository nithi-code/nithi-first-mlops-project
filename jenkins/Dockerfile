# Base image: official Jenkins LTS
FROM jenkins/jenkins:lts

USER root
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies (Python, Git, Docker CLI, curl, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        curl \
        git \
        docker.io \
    && rm -rf /var/lib/apt/lists/*

# Install Docker Compose manually
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Verify installations
RUN docker --version && docker-compose --version && python3 --version && pip3 --version

# Allow Jenkins user to use Docker safely
ARG DOCKER_GID=999
RUN groupadd -g $DOCKER_GID docker || true && \
    usermod -aG docker jenkins && \
    mkdir -p /var/jenkins_home && \
    chown -R jenkins:jenkins /var/jenkins_home

USER jenkins
WORKDIR /var/jenkins_home

# Expose Jenkins web UI
EXPOSE 8080

# Correct entrypoint for Jenkins
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/local/bin/jenkins.sh"]
