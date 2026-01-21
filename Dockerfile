FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libxcb-xinerama0 \
    libxcb-randr0 \
    libxcb-xtest0 \
    libxcb-shape0 \
    libxcb-xkb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxkbcommon-x11-0 \
    libx11-6 \
    libx11-xcb1 \
    libgl1-mesa-glx \
    libegl1-mesa \
    libfontconfig1 \
    libfreetype6 \
    libdbus-1-3 \
    libqt6core6t64 \
    libqt6gui6t64 \
    libqt6widgets6t64 \
    libqt6network6t64 \
    libqt6printsupport6t64 \
    libqt6svg6t64 \
    qt6-base-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

# Copy source code
COPY . .

# Build the application
RUN python3 build.py

# Set display for headless operation
ENV DISPLAY=:99
RUN Xvfb :99 -screen 0 1024x768x24 &

# Default command
CMD ["python3", "build.py"]