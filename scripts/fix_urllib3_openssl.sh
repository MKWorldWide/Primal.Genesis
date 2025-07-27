#!/bin/bash

# Function to fix urllib3/OpenSSL compatibility on a remote server
fix_urllib3_openssl() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Fixing urllib3/OpenSSL compatibility on $friendly_name ($instance_id) ==="
    
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
    
    # Create a temporary directory for the fix script
    local temp_dir=$(mktemp -d)
    
    # Create the fix script
    local fix_script="$temp_dir/fix_urllib3.sh"
    cat > "$fix_script" << 'EOF'
#!/bin/bash

# Exit on error
set -e

echo "Fixing urllib3/OpenSSL compatibility..."

# Check current OpenSSL version
echo "Current OpenSSL version:"
openssl version

# Check current Python and pip versions
echo -e "\nPython version:"
python3 --version

echo -e "\npip version:"
pip3 --version

# Check current urllib3 version
echo -e "\nCurrent urllib3 version:"
pip3 show urllib3 2>/dev/null || echo "urllib3 not found"

# Install a compatible version of urllib3
echo -e "\nInstalling urllib3 version compatible with OpenSSL 1.0.2..."
sudo pip3 install --upgrade 'urllib3<2.0.0' --force-reinstall

# Verify the installed version
echo -e "\nUpdated urllib3 version:"
pip3 show urllib3

# Get the service name from the current directory
cd /home/ec2-user/Primal-Genesis-Engine-Sovereign
SERVICE_NAME="$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr -d '-_')"

# Restart the service
echo -e "\nRestarting $SERVICE_NAME service..."
sudo systemctl restart "$SERVICE_NAME"

echo "$SERVICE_NAME service restarted!"

# Verify the service status
echo -e "\nVerifying service status..."
sudo systemctl status "$SERVICE_NAME" --no-pager

# Check if the service is running
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo -e "\n✅ $SERVICE_NAME is running!"
else
    echo -e "\n❌ $SERVICE_NAME failed to start. Check the logs with: sudo journalctl -u $SERVICE_NAME -n 50"
    exit 1
fi

echo -e "\nurllib3/OpenSSL compatibility fix complete!"
EOF
    
    # Make the fix script executable
    chmod +x "$fix_script"
    
    # Copy the fix script to the instance
    echo "Copying fix script to $friendly_name..."
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$fix_script" "ec2-user@$public_ip:~/fix_urllib3.sh"
    
    # Make the fix script executable on the remote server
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "chmod +x ~/fix_urllib3.sh"
    
    # Execute the fix script on the instance
    echo "Running fix script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "~/fix_urllib3.sh"
    
    # Clean up
    rm -rf "$temp_dir"
    
    echo "\nurllib3/OpenSSL compatibility fix applied on $friendly_name!"
}

# Main script
echo "Starting urllib3/OpenSSL compatibility fix on all servers..."

# Fix AthenaCore-Server
echo "\n===== Fixing AthenaCore-Server ====="
fix_urllib3_openssl "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Fix Lilithos-server
echo "\n===== Fixing Lilithos-server ====="
fix_urllib3_openssl "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nurllib3/OpenSSL compatibility fix complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
