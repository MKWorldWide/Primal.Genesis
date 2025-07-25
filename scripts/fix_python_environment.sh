#!/bin/bash

# Function to fix Python environment on an EC2 instance
fix_python_environment() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Fixing Python environment on $friendly_name ($instance_id) ==="
    
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

# Function to install Python 3.8 using Amazon Linux 2 extras
install_python38_amazon_linux() {
    echo "Installing Python 3.8 using Amazon Linux 2 extras..."
    
    # Enable the EPEL repository
    sudo amazon-linux-extras enable python3.8
    
    # Install Python 3.8
    sudo yum clean metadata
    sudo yum install -y python3.8
    
    # Install pip for Python 3.8
    curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.8
    
    # Install virtualenv
    sudo /usr/local/bin/pip3.8 install virtualenv
    
    echo "Python 3.8 installed successfully!"
}

# Function to create a virtual environment and install dependencies
setup_virtualenv() {
    local app_dir="$1"
    
    echo "Setting up Python virtual environment in $app_dir/venv..."
    
    # Create virtual environment
    /usr/local/bin/python3.8 -m virtualenv "$app_dir/venv"
    
    # Activate virtual environment and install dependencies
    source "$app_dir/venv/bin/activate"
    
    echo "Installing Python dependencies in virtual environment..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install required packages
    pip install fastapi uvicorn jinja2 websockets pydantic requests
    
    # Install any additional requirements if requirements.txt exists
    if [ -f "$app_dir/requirements.txt" ]; then
        echo "Installing requirements from requirements.txt..."
        pip install -r "$app_dir/requirements.txt"
    fi
    
    deactivate
    
    echo "Virtual environment setup complete!"
}

# Function to update systemd service file
update_service_file() {
    local service_name="$1"
    local app_dir="$2"
    
    echo "Updating $service_name systemd service file..."
    
    # Create the service file with the correct Python path
    sudo tee "/etc/systemd/system/$service_name.service" > /dev/null <<SERVICE_EOF
[Unit]
Description=${service_name^} Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=${app_dir}
Environment="PYTHONPATH=${app_dir}:${app_dir}/src"
ExecStart=${app_dir}/venv/bin/python3 ${app_dir}/run_web_interface.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    echo "$service_name service file updated!"
}

# Main script
echo "Starting Python environment fix..."

# Install Python 3.8 if not already installed
if ! command -v python3.8 &> /dev/null; then
    echo "Python 3.8 not found, installing..."
    install_python38_amazon_linux
else
    echo "Python 3.8 is already installed."
fi

# Set the application directory
APP_DIR="$HOME/Primal-Genesis-Engine-Sovereign"

# Create the application directory if it doesn't exist
mkdir -p "$APP_DIR"

# Set up virtual environment and install dependencies
setup_virtualenv "$APP_DIR"

# Get the service name from the current directory name
SERVICE_NAME="$(basename "$APP_DIR" | tr '[:upper:]' '[:lower:]' | tr -d '-_')"

# Update the systemd service file
update_service_file "$SERVICE_NAME" "$APP_DIR"

# Restart the service
echo "Restarting $SERVICE_NAME service..."
sudo systemctl restart "$SERVICE_NAME"

# Check service status
echo "$SERVICE_NAME service status:"
sleep 2  # Give the service a moment to start
sudo systemctl status "$SERVICE_NAME" --no-pager

echo "\nPython environment fix complete!"
EOF
    
    # Make the script executable and copy it to the instance
    chmod +x "$temp_script"
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:fix_python.sh"
    
    # Execute the script on the instance
    echo "Running Python environment fix script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "./fix_python.sh"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\nPython environment fix complete for $friendly_name!"
}

# Main script
echo "Starting Python environment fix for all servers..."

# Fix Python environment on AthenaCore-Server
echo "\n===== Fixing Python Environment on AthenaCore-Server ====="
fix_python_environment "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Fix Python environment on Lilithos-server
echo "\n===== Fixing Python Environment on Lilithos-server ====="
fix_python_environment "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nPython environment fix complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
