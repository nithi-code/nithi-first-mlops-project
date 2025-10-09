# ================================
# Jenkins with Docker, Python, and Docker Compose
# ================================
FROM jenkins/jenkins:lts

USER root
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies: Python, Git, Docker CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        curl \
        git \
        docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Install Docker Compose (latest stable release)
# -------------------------------
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# -------------------------------
# Setup Python virtual environment
# -------------------------------
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip

ENV PATH="/opt/venv/bin:$PATH"

# -------------------------------
# Allow Jenkins to access Docker socket
# -------------------------------
ARG DOCKER_GID=999
RUN groupadd -g $DOCKER_GID docker || true && \
    usermod -aG docker jenkins && \
    mkdir -p /var/jenkins_home && \
    chown -R jenkins:jenkins /var/jenkins_home

USER jenkins
WORKDIR /var/jenkins_home

# Expose Jenkins UI
EXPOSE 8080

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/local/bin/jenkins.sh"]
