#!/bin/bash
set -e

echo "Starting setup..."

# Detect user and home directory
USER_HOME=$(eval echo ~${SUDO_USER:-$USER})
USERNAME=$(basename "$USER_HOME")
PROJECT_DIR="$USER_HOME/Focus-Timer"
LOG_FILE="/var/log/focus-timer.log"

# 1. Install system packages
echo "Installing system packages..."
sudo apt update
sudo apt install -y \
  python3-pip \
  python3-opencv \
  python3-pil \
  python3-gpiozero \
  python3-spidev \
  python3-numpy \
  python3-smbus \

# 2. Enable SPI
echo "Enabling SPI..."
sudo raspi-config nonint do_spi 0

# 4. Create systemd service
SERVICE_PATH="/etc/systemd/system/focus-timer.service"

echo "Creating systemd service at $SERVICE_PATH..."

cat <<EOF | sudo tee $SERVICE_PATH > /dev/null
[Unit]
Description=Focus Timer with OLED Display
After=network.target

[Service]
ExecStart=/usr/bin/python3 $PROJECT_DIR/main.py
WorkingDirectory=$PROJECT_DIR
StandardOutput=file:$LOG_FILE
StandardError=inherit
Restart=always
User=$USERNAME
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# 5. Enable and start the service
echo "Enabling focus-timer service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable focus-timer.service
sudo systemctl start focus-timer.service

echo "Setup complete!"
echo "Log output: sudo journalctl -u focus-timer.service -f"
