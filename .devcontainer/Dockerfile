# Base image with Python 3.13
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Tokyo \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_SYSTEM_PYTHON=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build essentials
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    # Git and version control
    git \
    git-lfs \
    # Network tools
    curl \
    wget \
    ca-certificates \
    gnupg \
    lsb-release \
    # Development tools
    vim \
    nano \
    less \
    htop \
    tree \
    jq \
    ripgrep \
    fd-find \
    # Python development
    python3-dev \
    python3-pip \
    python3-venv \
    # Libraries for common Python packages
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js LTS for Pyright
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pyright \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Rust-based Python package manager)
# Copy uv binary from official distroless image
COPY --from=ghcr.io/astral-sh/uv:0.8.7 /uv /uvx /bin/

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install global Python tools using uv
RUN uv tool install ruff && \
    uv tool install pytest && \
    uv tool install sphinx && \
    uv tool install ipython && \
    uv tool install jupyterlab && \
    uv tool install pre-commit

# Add UV tools to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy and install common team libraries
COPY requirements-common.txt /tmp/requirements-common.txt

# Pre-download common Python packages as root
# Install from requirements-common.txt for consistency
RUN uv pip install --system -r /tmp/requirements-common.txt && \
    rm /tmp/requirements-common.txt

# Create workspace directory
RUN mkdir -p /workspace && \
    chown -R $USERNAME:$USERNAME /workspace

# Switch to non-root user
USER $USERNAME

# Set working directory
WORKDIR /workspace

# Install user-level tools
RUN echo 'export PATH="/home/vscode/.local/bin:$PATH"' >> /home/vscode/.bashrc && \
    echo 'alias ll="ls -la"' >> /home/vscode/.bashrc && \
    echo 'alias ..="cd .."' >> /home/vscode/.bashrc && \
    echo 'alias ...="cd ../.."' >> /home/vscode/.bashrc && \
    echo 'alias gs="git status"' >> /home/vscode/.bashrc && \
    echo 'alias gd="git diff"' >> /home/vscode/.bashrc && \
    echo 'alias gc="git commit"' >> /home/vscode/.bashrc && \
    echo 'alias gp="git push"' >> /home/vscode/.bashrc && \
    echo 'alias gl="git log --oneline --graph --decorate"' >> /home/vscode/.bashrc

# Configure git
RUN git config --global init.defaultBranch main && \
    git config --global core.editor vim && \
    git config --global pull.rebase false

# Expose common ports
EXPOSE 8000 8080 8888 5000 3000

# Default command
CMD ["/bin/bash"]