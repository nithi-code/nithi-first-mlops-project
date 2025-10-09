# Base image: Jenkins LTS
FROM jenkins/jenkins:lts

USER root
ENV DEBIAN_FRONTEND=noninteractive

# ------------------------
# Install system dependencies: Python, Git, Docker CLI
# ------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        curl \
        git \
        sudo \
        gnupg \
        lsb-release \
        ca-certificates \
        apt-transport-https \
        software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# ------------------------
# Install Docker CLI (from Docker repository)
# ------------------------
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli

# ------------------------
# Install Docker Compose
# ------------------------
RUN curl -L "https://github.com/docker/compose/releases/download/v2.21.1/docker-compose-linux-x86_64" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# ------------------------
# Create Python virtual environment
# ------------------------
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip

ENV PATH="/opt/venv/bin:$PATH"

# ------------------------
# Allow Jenkins user to use Docker safely
# ------------------------
ARG DOCKER_GID=999
RUN groupadd -g $DOCKER_GID docker || true && \
    usermod -aG docker jenkins && \
    mkdir -p /var/jenkins_home && chown -R jenkins:jenkins /var/jenkins_home

# ------------------------
# Switch back to Jenkins user
# ------------------------
USER jenkins
WORKDIR /var/jenkins_home

# Expose Jenkins UI and agent port
EXPOSE 8080 50000

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/local/bin/jenkins.sh"]
