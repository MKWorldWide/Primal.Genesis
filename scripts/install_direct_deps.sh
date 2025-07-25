#!/bin/bash

# Function to install dependencies directly on an EC2 instance
install_direct_deps() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Installing dependencies directly on $friendly_name ($instance_id) ==="
    
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

echo "Installing system dependencies..."
sudo yum update -y
sudo yum install -y python3-pip python3-devel gcc

# Install Python 3.8 if not already installed
if ! command -v python3.8 &> /dev/null; then
    echo "Installing Python 3.8..."
    sudo amazon-linux-extras enable python3.8
    sudo yum clean metadata
    sudo yum install -y python3.8
    
    # Install pip for Python 3.8
    curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.8
    
    # Create a symlink from python3 to python3.8
    sudo ln -sf /usr/bin/python3.8 /usr/bin/python3
    
    echo "Python 3.8 installed successfully!"
else
    echo "Python 3.8 is already installed."
fi

# Install required packages with the correct Python version
echo "Installing required Python packages..."
sudo python3.8 -m pip install --upgrade pip

# Install specific versions known to work with Python 3.8
sudo python3.8 -m pip install \
    fastapi==0.95.2 \
    uvicorn==0.22.0 \
    jinja2==3.1.2 \
    websockets==10.4 \
    pydantic==1.10.7 \
    requests==2.31.0

echo "Dependencies installed successfully!"

# Update the systemd service to use Python 3.8
echo "Updating systemd service to use Python 3.8..."

# Get the service name from the current directory
SERVICE_NAME="$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr -d '-_')"

# Create or update the service file
sudo tee "/etc/systemd/system/$SERVICE_NAME.service" > /dev/null <<SERVICE_EOF
[Unit]
Description=${SERVICE_NAME^} Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=$(pwd)
Environment="PYTHONPATH=$(pwd):$(pwd)/src"
ExecStart=/usr/bin/python3.8 $(pwd)/run_web_interface.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable and restart the service
echo "Restarting $SERVICE_NAME service..."
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "$SERVICE_NAME service restarted!"

echo "Installation and configuration complete!"
EOF
    
    # Make the script executable and copy it to the instance
    chmod +x "$temp_script"
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:install_deps.sh"
    
    # Execute the script on the instance
    echo "Running dependency installation script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "./install_deps.sh"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\nDependency installation complete for $friendly_name!"
}

# Main script
echo "Starting direct dependency installation..."

# Install dependencies on AthenaCore-Server
echo "\n===== Installing Dependencies on AthenaCore-Server ====="
install_direct_deps "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Install dependencies on Lilithos-server
echo "\n===== Installing Dependencies on Lilithos-server ====="
install_direct_deps "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nDependency installation complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
