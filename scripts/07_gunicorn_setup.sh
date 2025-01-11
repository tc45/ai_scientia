#!/bin/bash

log_message "Starting Gunicorn Setup..."

# Create Gunicorn systemd service file
log_message "Creating Gunicorn systemd service file..."
sudo tee /etc/systemd/system/${PROJECT_NAME,,}.service > /dev/null << EOF
[Unit]
Description=$PROJECT_NAME Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$INSTALL_PATH/src
Environment="PATH=$INSTALL_PATH/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="DJANGO_SETTINGS_MODULE=${PROJECT_NAME,,}.settings.development"
Environment="PYTHONUNBUFFERED=1"
Environment="PYTHONDONTWRITEBYTECODE=1"
Environment="DJANGO_PORT=${DJANGO_PORT:-8000}"

ExecStart=$INSTALL_PATH/venv/bin/gunicorn \
    ${PROJECT_NAME,,}.wsgi:application \
    --bind 0.0.0.0:${DJANGO_PORT:-8000} \
    --workers 2 \
    --worker-connections=1000 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --timeout 30 \
    --keep-alive 5 \
    --log-level=info \
    --reload

# Improve service reliability
Restart=always
RestartSec=3
TimeoutStopSec=5

[Install]
WantedBy=multi-user.target
EOF

# Set proper permissions
log_message "Setting service file permissions..."
sudo chmod 644 /etc/systemd/system/${PROJECT_NAME,,}.service

# Set proper ownership
log_message "Setting project directory ownership..."
sudo chown -R www-data:www-data $INSTALL_PATH

# Reload systemd and start service
log_message "Reloading systemd daemon..."
sudo systemctl daemon-reload >> "$LOG_FILE" 2>&1

log_message "Enabling Gunicorn service..."
sudo systemctl enable ${PROJECT_NAME,,} >> "$LOG_FILE" 2>&1

log_message "Starting Gunicorn service..."
sudo systemctl start ${PROJECT_NAME,,} >> "$LOG_FILE" 2>&1

log_message "Checking Gunicorn service status..."
sudo systemctl status ${PROJECT_NAME,,} >> "$LOG_FILE" 2>&1

# Verify service is running
if ! sudo systemctl is-active --quiet ${PROJECT_NAME,,}; then
    log_message "ERROR: Failed to start Gunicorn service"
    log_message "$(sudo systemctl status ${PROJECT_NAME,,})"
    log_message "Check logs with: sudo journalctl -u ${PROJECT_NAME,,} -f"
    exit 1
fi

# Verify port is in use
if ! sudo netstat -tulpn | grep ${DJANGO_PORT:-8000} >> "$LOG_FILE" 2>&1; then
    log_message "WARNING: Port ${DJANGO_PORT:-8000} does not appear to be in use"
fi

log_message "Gunicorn Setup completed successfully"