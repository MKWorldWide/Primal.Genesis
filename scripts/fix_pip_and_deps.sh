#!/bin/bash

# Function to fix pip and install dependencies on an EC2 instance
fix_pip_and_deps() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Fixing pip and installing dependencies on $friendly_name ($instance_id) ==="
    
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

echo "Fixing pip installation for Python 3.8..."

# Install pip for Python 3.8 using the correct bootstrap script
curl -sS https://bootstrap.pypa.io/pip/3.8/get-pip.py | sudo python3.8

# Ensure pip is in the PATH
export PATH="$HOME/.local/bin:$PATH"

# Upgrade pip to the latest version
echo "Upgrading pip..."
python3.8 -m pip install --upgrade pip

# Install required packages
echo "Installing required Python packages..."
python3.8 -m pip install --user fastapi uvicorn jinja2 websockets pydantic requests

# Create a symlink to ensure python3 points to python3.8
echo "Ensuring python3 points to python3.8..."
sudo ln -sf /usr/bin/python3.8 /usr/bin/python3

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
Environment="PATH=/home/ec2-user/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/usr/bin/python3.8 $(pwd)/run_web_interface.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Reload systemd
sudo systemctl daemon-reload

# Restart the service
echo "Restarting $SERVICE_NAME service..."
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "$SERVICE_NAME service restarted!"

echo "Verifying service status..."
sudo systemctl status $SERVICE_NAME --no-pager

echo "Installation and configuration complete!"
EOF
    
    # Make the script executable and copy it to the instance
    chmod +x "$temp_script"
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:fix_pip.sh"
    
    # Execute the script on the instance
    echo "Running pip and dependency fix script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "./fix_pip.sh"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\nPip and dependency fix complete for $friendly_name!"
}

# Main script
echo "Starting pip and dependency fix for all servers..."

# Fix pip and install dependencies on AthenaCore-Server
echo "\n===== Fixing pip and dependencies on AthenaCore-Server ====="
fix_pip_and_deps "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Fix pip and install dependencies on Lilithos-server
echo "\n===== Fixing pip and dependencies on Lilithos-server ====="
fix_pip_and_deps "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nPip and dependency fix complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
