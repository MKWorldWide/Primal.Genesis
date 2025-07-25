#!/bin/bash

# Configuration
INSTANCE_ID="i-06d885a2cfb302317"
SSH_KEY="$HOME/.ssh/lilithos-key-new.pem"
SSH_USER="ec2-user"
REPO_URL="https://github.com/MKWorldWide/Primal-Genesis-Engine-Sovereign.git"
APP_DIR="Primal-Genesis-Engine-Sovereign"

# Get the public IP of the instance
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

if [ -z "$PUBLIC_IP" ] || [ "$PUBLIC_IP" = "None" ]; then
    echo "Error: Could not get public IP for instance $INSTANCE_ID"
    exit 1
fi

echo "Deploying to Lilithos-server ($PUBLIC_IP)..."

# Create a temporary script to run on the instance
deploy_script=$(cat << 'EOF'
#!/bin/bash

# Exit on error
set -e

# Configuration
REPO_URL="https://github.com/MKWorldWide/Primal-Genesis-Engine-Sovereign.git"
APP_DIR="Primal-Genesis-Engine-Sovereign"

# Update package lists and install dependencies
echo "Updating system packages..."
sudo yum update -y

# Install required packages
echo "Installing required packages..."
sudo yum install -y git python3 python3-pip python3-devel gcc

# Clone or update the repository
if [ -d "$APP_DIR" ]; then
    echo "Updating repository..."
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

# Install a compatible version of requests for Python 3.7
echo "Installing compatible version of requests..."
python3 -m pip install 'requests>=2.27.0,<2.32.0' --user

# Install other requirements, skipping any that fail
echo "Installing other requirements..."
python3 -m pip install -r requirements.txt --user || echo "Warning: Some dependencies may not have installed correctly"

# Set up the LilithOS service
echo "Setting up LilithOS service..."
sudo tee /etc/systemd/system/lilithos.service > /dev/null <<SERVICE_EOF
[Unit]
Description=LilithOS Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/$APP_DIR
ExecStart=/usr/bin/python3 -m lilithos.app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Reload systemd and enable/restart the service
echo "Starting LilithOS service..."
sudo systemctl daemon-reload
sudo systemctl enable lilithos
sudo systemctl restart lilithos

# Check service status
echo "LilithOS service status:"
sudo systemctl status lilithos --no-pager

echo "\nDeployment completed successfully!"
EOF
)

# Execute the deployment script on the remote instance
echo "Starting deployment on Lilithos-server..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$PUBLIC_IP" "bash -s" <<< "$deploy_script"

echo "\nLilithOS deployment completed!"
echo "You can access LilithOS at: http://$PUBLIC_IP:8000"
