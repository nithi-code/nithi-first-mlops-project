FROM jenkins/jenkins:lts

USER root
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, Git, Docker CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        curl \
        git \
        docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Install Docker Compose (latest release)
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose && \
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose && \
    echo 'alias docker-compose="docker compose"' >> /etc/bash.bashrc

# Ensure compose is available globally
ENV PATH="/usr/local/bin:${PATH}"

# Optional: check installations
RUN docker-compose version && docker --version && python3 --version && pip3 --version

# Docker socket permissions
ARG DOCKER_GID=999
RUN groupadd -g $DOCKER_GID docker || true && \
    usermod -aG docker jenkins && \
    mkdir -p /var/jenkins_home && \
    chown -R jenkins:jenkins /var/jenkins_home

USER jenkins
WORKDIR /var/jenkins_home
EXPOSE 8080

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/local/bin/jenkins.sh"]
