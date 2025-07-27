#!/bin/bash

# Function to install Python 3.8 on an EC2 instance
install_python38() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Installing Python 3.8 on $friendly_name ($instance_id) ==="
    
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

echo "Updating package lists..."
sudo yum update -y

echo "Enabling Python 3.8 Amazon Linux 2 extras..."
sudo amazon-linux-extras enable python3.8

# Clean yum metadata to ensure the new repo is picked up
echo "Cleaning yum metadata..."
sudo yum clean metadata

# Install Python 3.8
echo "Installing Python 3.8..."
sudo yum install -y python3.8

# Create a symlink from python3 to python3.8
echo "Creating symlinks..."
sudo ln -sf /usr/bin/python3.8 /usr/bin/python3

# Install pip for Python 3.8
echo "Installing pip for Python 3.8..."
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.8

# Verify installation
echo -n "Python 3.8 version: "
python3.8 --version
echo -n "Python 3 version: "
python3 --version
echo -n "Pip version: "
pip3 --version

echo "Python 3.8 installation complete!"

# Install required packages
echo "Installing required Python packages..."
sudo python3.8 -m pip install --upgrade pip
sudo python3.8 -m pip install fastapi uvicorn jinja2 websockets pydantic requests

echo "Python packages installed successfully!"

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
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:install_python38.sh"
    
    # Execute the script on the instance
    echo "Running Python 3.8 installation script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "./install_python38.sh"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\nPython 3.8 installation complete for $friendly_name!"
}

# Main script
echo "Starting Python 3.8 installation on all servers..."

# Install Python 3.8 on AthenaCore-Server
echo "\n===== Installing Python 3.8 on AthenaCore-Server ====="
install_python38 "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Install Python 3.8 on Lilithos-server
echo "\n===== Installing Python 3.8 on Lilithos-server ====="
install_python38 "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nPython 3.8 installation complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
