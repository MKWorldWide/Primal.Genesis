#!/bin/bash

# Function to set up a service on an EC2 instance
setup_service() {
    local instance_id="$1"
    local ssh_key="$2"
    local service_name="$3"
    local friendly_name="$4"
    local app_module="$5"
    
    echo "\n=== Setting up $friendly_name ($instance_id) ==="
    
    # Get the public IP of the instance
    local public_ip=$(aws ec2 describe-instances \
        --instance-ids "$instance_id" \
        --query 'Reservations[0].Instances[0].PublicIpAddress' \
        --output text)
    
    if [ -z "$public_ip" ] || [ "$public_ip" = "None" ]; then
        echo "Error: Could not get public IP for instance $instance_id"
        return 1
    fi
    
    echo "Instance IP: $public_ip"
    
    # Create a temporary script to run on the instance
    local temp_script=$(mktemp)
    cat > "$temp_script" << 'EOF'
#!/bin/bash

# Exit on error
set -e

# Configuration
SERVICE_NAME="$1"
FRIENDLY_NAME="$2"
APP_MODULE="$3"
APP_DIR="$HOME/Primal-Genesis-Engine-Sovereign"
SERVICE_USER="ec2-user"

# Create the service file
echo "Creating $SERVICE_NAME service file..."
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<SERVICE_EOF
[Unit]
Description=${FRIENDLY_NAME} Service
After=network.target

[Service]
User=${SERVICE_USER}
WorkingDirectory=${APP_DIR}
Environment="PYTHONPATH=${APP_DIR}"
ExecStart=/usr/bin/python3 -m ${APP_MODULE} run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Reload systemd
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable and start the service
echo "Enabling and starting $SERVICE_NAME service..."
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl restart ${SERVICE_NAME}

# Check service status
echo "$SERVICE_NAME service status:"
sudo systemctl status ${SERVICE_NAME} --no-pager

echo "\n$FRIENDLY_NAME service setup complete!"
EOF
    
    # Make the script executable and copy it to the instance
    chmod +x "$temp_script"
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:setup_service.sh"
    
    # Execute the script on the instance
    echo "Running setup script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "./setup_service.sh $service_name '$friendly_name' $app_module"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\n$friendly_name service setup complete!"
}

# Main script
echo "Starting manual service setup..."

# Set up AthenaCore service
echo "\n===== Setting up AthenaCore Service ====="
setup_service "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" \
    "athenacore" "AthenaCore-Server" "athenacore.app"

# Set up LilithOS service
echo "\n===== Setting up LilithOS Service ====="
setup_service "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" \
    "lilithos" "Lilithos-server" "lilithos.app"

echo "\nService setup complete! Verifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
