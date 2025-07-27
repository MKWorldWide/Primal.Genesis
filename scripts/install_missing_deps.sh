#!/bin/bash

# Function to install missing dependencies on an EC2 instance
install_missing_deps() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Installing missing dependencies on $friendly_name ($instance_id) ==="
    
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

echo "Installing missing dependencies..."

# Install aiohttp and other missing dependencies
python3.8 -m pip install --user aiohttp aiofiles python-multipart

# Get the service name from the current directory
SERVICE_NAME="$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr -d '-_')"

# Restart the service
echo "Restarting $SERVICE_NAME service..."
sudo systemctl restart $SERVICE_NAME

echo "$SERVICE_NAME service restarted!"

echo "Verifying service status..."
sudo systemctl status $SERVICE_NAME --no-pager

echo "Installation and service restart complete!"
EOF
    
    # Make the script executable and copy it to the instance
    chmod +x "$temp_script"
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:install_missing_deps.sh"
    
    # Execute the script on the instance
    echo "Running missing dependency installation script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "./install_missing_deps.sh"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\nMissing dependency installation complete for $friendly_name!"
}

# Main script
echo "Starting missing dependency installation for all servers..."

# Install missing dependencies on AthenaCore-Server
echo "\n===== Installing missing dependencies on AthenaCore-Server ====="
install_missing_deps "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Install missing dependencies on Lilithos-server
echo "\n===== Installing missing dependencies on Lilithos-server ====="
install_missing_deps "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nMissing dependency installation complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
