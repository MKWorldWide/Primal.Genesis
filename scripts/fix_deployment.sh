#!/bin/bash

# Function to fix deployment on an EC2 instance
fix_deployment() {
    local instance_id="$1"
    local ssh_key="$2"
    local service_name="$3"
    local friendly_name="$4"
    
    echo "\n=== Fixing $friendly_name ($instance_id) ==="
    
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
REPO_URL="https://github.com/MKWorldWide/Primal-Genesis-Engine-Sovereign.git"
APP_DIR="Primal-Genesis-Engine-Sovereign"
SERVICE_NAME="$1"
FRIENDLY_NAME="$2"

# Update package lists and install dependencies
echo "Updating system packages..."
sudo yum update -y

# Install required packages
echo "Installing required packages..."
sudo yum install -y git python3 python3-pip python3-devel gcc

# Clone or update the repository
echo "Setting up application directory..."
if [ -d "$APP_DIR" ]; then
    echo "Updating existing repository..."
    cd "$APP_DIR"
    git fetch --all
    git reset --hard origin/main
    git pull origin main
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install --user -r requirements.txt

# Create the service file
echo "Creating $SERVICE_NAME service..."
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<SERVICE_EOF
[Unit]
Description=${FRIENDLY_NAME} Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/${APP_DIR}
Environment="PYTHONPATH=/home/ec2-user/${APP_DIR}"
ExecStart=/usr/bin/python3 -m athenacore.app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Reload systemd and enable/start the service
echo "Starting $SERVICE_NAME service..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl restart ${SERVICE_NAME}

# Check service status
echo "$SERVICE_NAME service status:"
sudo systemctl status ${SERVICE_NAME} --no-pager

echo "\n$FRIENDLY_NAME deployment fixed successfully!"
EOF
    
    # Execute the script on the instance
    echo "Running fix script on $friendly_name..."
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:fix_script.sh"
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "chmod +x fix_script.sh && ./fix_script.sh $service_name '$friendly_name'"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\n$friendly_name fix completed!"
}

# Main script
echo "Starting deployment fix..."

# Fix AthenaCore-Server
echo "\n===== Fixing AthenaCore-Server ====="
fix_deployment "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" \
    "athenacore" "AthenaCore-Server"

# Fix Lilithos-server
echo "\n===== Fixing Lilithos-server ====="
fix_deployment "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" \
    "lilithos" "Lilithos-server"

echo "\nDeployment fix complete! Verifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
