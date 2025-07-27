#!/bin/bash

# Function to resolve dependency issues on an EC2 instance
resolve_dependencies() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Resolving dependencies on $friendly_name ($instance_id) ==="
    
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

# Function to install Python 3.8
install_python38() {
    echo "Installing Python 3.8..."
    # Install required packages
    sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel
    
    # Download and install Python 3.8
    cd /tmp
    curl -O https://www.python.org/ftp/python/3.8.18/Python-3.8.18.tgz
    tar xzf Python-3.8.18.tgz
    cd Python-3.8.18
    ./configure --enable-optimizations
    make -j $(nproc)
    sudo make altinstall
    
    # Verify installation
    python3.8 --version
    
    # Install pip for Python 3.8
    curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.8
    
    echo "Python 3.8 installed successfully!"
}

# Function to install compatible package versions for Python 3.7
install_compatible_packages() {
    echo "Installing compatible package versions for Python 3.7..."
    
    # Create a temporary requirements file with compatible versions
    cat > /tmp/compatible_requirements.txt << 'REQ_EOF'
fastapi==0.95.2
uvicorn==0.22.0
jinja2==3.1.2
websockets==10.4
pydantic==1.10.7
requests==2.31.0
REQ_EOF
    
    # Install the packages
    python3 -m pip install --upgrade pip
    python3 -m pip install -r /tmp/compatible_requirements.txt --user
    
    echo "Compatible packages installed successfully!"
}

# Main script
echo "Resolving dependency issues..."

# Check current Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Current Python version: $PYTHON_VERSION"

# Try to install Python 3.8 if not already installed
if [[ "$PYTHON_VERSION" < "3.8" ]]; then
    echo "Python version is less than 3.8, attempting to install Python 3.8..."
    
    if ! command -v python3.8 &> /dev/null; then
        install_python38
    else
        echo "Python 3.8 is already installed."
    fi
    
    # Update the systemd service to use Python 3.8
    echo "Updating systemd service to use Python 3.8..."
    sudo sed -i 's|/usr/bin/python3|/usr/local/bin/python3.8|' /etc/systemd/system/*.service
    sudo systemctl daemon-reload
    
    # Install packages with Python 3.8
    echo "Installing required packages with Python 3.8..."
    python3.8 -m pip install --upgrade pip
    python3.8 -m pip install fastapi uvicorn jinja2 websockets pydantic requests
else
    # Install compatible packages for Python 3.7
    install_compatible_packages
fi

echo "Dependency resolution complete!"

# Restart the service
SERVICE_NAME=$(basename /etc/systemd/system/*.service .service | head -n 1)
echo "Restarting $SERVICE_NAME service..."
sudo systemctl restart $SERVICE_NAME

echo "Service $SERVICE_NAME restarted!"
EOF
    
    # Make the script executable and copy it to the instance
    chmod +x "$temp_script"
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:resolve_deps.sh"
    
    # Execute the script on the instance
    echo "Running dependency resolution script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "./resolve_deps.sh"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\nDependency resolution complete for $friendly_name!"
}

# Main script
echo "Starting dependency resolution..."

# Resolve dependencies on AthenaCore-Server
echo "\n===== Resolving Dependencies on AthenaCore-Server ====="
resolve_dependencies "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Resolve dependencies on Lilithos-server
echo "\n===== Resolving Dependencies on Lilithos-server ====="
resolve_dependencies "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nDependency resolution complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
