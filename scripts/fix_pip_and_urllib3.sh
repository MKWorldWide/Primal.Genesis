#!/bin/bash

# Function to fix pip3 and urllib3 on a remote server
fix_remote_pip_urllib3() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Fixing pip3 and urllib3 on $friendly_name ($instance_id) ==="
    
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
    local fix_script="$temp_dir/fix_pip_urllib3.sh"
    cat > "$fix_script" << 'EOF'
#!/bin/bash

# Exit on error
set -e

echo "=== Starting pip3 and urllib3 fix ==="

# Check current user
echo "Current user: $(whoami)"

# Check Python and pip versions
echo -e "\n=== Python and pip versions ==="
python3 --version || echo "Python3 not found"
which python3 || echo "python3 not in PATH"

# Find all python3 and pip3 executables
echo -e "\n=== Python and pip executables ==="
find / -name python3 -type f 2>/dev/null | grep -v "mozilla" | head -10
echo "---"
find / -name pip3 -type f 2>/dev/null | grep -v "mozilla" | head -10

# Install pip3 using ensurepip if not found
if ! command -v pip3 &> /dev/null; then
    echo -e "\n=== Installing pip3 using ensurepip ==="
    python3 -m ensurepip --upgrade --default-pip
    
    # Add pip3 to PATH if needed
    if [ -f "$HOME/.local/bin/pip3" ] && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo "Adding $HOME/.local/bin to PATH"
        export PATH="$HOME/.local/bin:$PATH"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    fi
    
    # Verify pip3 installation
    if ! command -v pip3 &> /dev/null; then
        echo -e "\n=== Installing pip3 using get-pip.py ==="
        curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
        python3 /tmp/get-pip.py --user
        rm /tmp/get-pip.py
    fi
fi

# Verify pip3 is available
echo -e "\n=== Verifying pip3 ==="
which pip3 || echo "pip3 still not found"
pip3 --version || echo "pip3 not working"

# Install urllib3<2.0.0
echo -e "\n=== Installing urllib3<2.0.0 ==="
# Try with --user first
if ! pip3 install --user 'urllib3<2.0.0' --force-reinstall; then
    echo "--user install failed, trying with sudo"
    # If that fails, try with sudo
    if command -v sudo &> /dev/null; then
        if ! sudo pip3 install 'urllib3<2.0.0' --force-reinstall; then
            echo "=== WARNING: Failed to install urllib3 with sudo ==="
            echo "Trying alternative installation method..."
            
            # Try using the system package manager
            if command -v yum &> /dev/null; then
                echo "Using yum to install python3-urllib3"
                sudo yum install -y python3-urllib3 || echo "yum install failed"
            elif command -v apt-get &> /dev/null; then
                echo "Using apt-get to install python3-urllib3"
                sudo apt-get update
                sudo apt-get install -y python3-urllib3 || echo "apt-get install failed"
            fi
            
            # Try one more time with pip3
            pip3 install --user 'urllib3<2.0.0' --force-reinstall || \
            echo "Final attempt to install urllib3 failed"
        fi
    else
        echo "sudo not available, trying without it"
        pip3 install --user 'urllib3<2.0.0' --force-reinstall || \
        echo "Failed to install urllib3 without sudo"
    fi
fi

# Verify urllib3 version
echo -e "\n=== Verifying urllib3 version ==="
python3 -c "import urllib3; print(f'urllib3 version: {urllib3.__version__}')" || \
echo "Failed to verify urllib3 version"

# Get the service name from the current directory
cd /home/ec2-user/Primal-Genesis-Engine-Sovereign
SERVICE_NAME="$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr -d '-_')"

# Restart the service
echo -e "\n=== Restarting $SERVICE_NAME service ==="
sudo systemctl daemon-reload
sudo systemctl restart "$SERVICE_NAME"

# Verify the service status
echo -e "\n=== Service status ==="
sudo systemctl status "$SERVICE_NAME" --no-pager

# Check if the service is running
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo -e "\n✅ $SERVICE_NAME is running!"
    # Check if the service is listening on port 8000
    if netstat -tuln | grep -q ':8000'; then
        echo "✅ Service is listening on port 8000"
    else
        echo "⚠️  Service is running but not listening on port 8000"
    fi
else
    echo -e "\n❌ $SERVICE_NAME failed to start. Checking logs..."
    sudo journalctl -u "$SERVICE_NAME" -n 20 --no-pager
fi

echo -e "\n=== Fix complete! ==="
EOF
    
    # Make the fix script executable
    chmod +x "$fix_script"
    
    # Copy the fix script to the instance
    echo "Copying fix script to $friendly_name..."
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$fix_script" "ec2-user@$public_ip:~/fix_pip_urllib3.sh"
    
    # Make the fix script executable on the remote server
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "chmod +x ~/fix_pip_urllib3.sh"
    
    # Execute the fix script on the instance
    echo "Running fix script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "~/fix_pip_urllib3.sh"
    
    # Clean up
    rm -rf "$temp_dir"
    
    echo "\n=== Fix completed on $friendly_name! ==="
}

# Main script
echo "Starting pip3 and urllib3 fix on all servers..."

# Fix AthenaCore-Server
echo "\n===== Fixing AthenaCore-Server ====="
fix_remote_pip_urllib3 "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Fix Lilithos-server
echo "\n===== Fixing Lilithos-server ====="
fix_remote_pip_urllib3 "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\n=== Verification in progress... ==="

# Verify the services
./scripts/verify_deployment.sh

echo "\n=== All done! Review the output above to ensure both services are running correctly. ==="
