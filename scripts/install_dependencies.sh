#!/bin/bash

# Function to install dependencies on an EC2 instance
install_dependencies() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Installing dependencies on $friendly_name ($instance_id) ==="
    
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

# Install required system packages
echo "Installing system dependencies..."
sudo yum update -y
sudo yum install -y python3-pip python3-devel gcc

# Install Python dependencies
echo "Installing Python dependencies..."
cd ~/Primal-Genesis-Engine-Sovereign

# Ensure pip is up to date
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    python3 -m pip install -r requirements.txt
else
    echo "requirements.txt not found, installing core dependencies directly..."
    python3 -m pip install fastapi uvicorn jinja2 websockets pydantic
fi

echo "Dependencies installed successfully!"
EOF
    
    # Make the script executable and copy it to the instance
    chmod +x "$temp_script"
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_script" "ec2-user@$public_ip:install_deps.sh"
    
    # Execute the script on the instance
    echo "Running dependency installation on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "./install_deps.sh"
    
    # Clean up
    rm -f "$temp_script"
    
    echo "\nDependency installation complete for $friendly_name!"
}

# Main script
echo "Starting dependency installation..."

# Install dependencies on AthenaCore-Server
echo "\n===== Installing Dependencies on AthenaCore-Server ====="
install_dependencies "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Install dependencies on Lilithos-server
echo "\n===== Installing Dependencies on Lilithos-server ====="
install_dependencies "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nDependency installation complete on all servers!"

echo "\nRestarting services..."

# Restart services
for instance_id in "i-01f16ff979f0934b1" "i-06d885a2cfb302317"; do
    friendly_name=""
    if [ "$instance_id" = "i-01f16ff979f0934b1" ]; then
        friendly_name="AthenaCore-Server"
        service_name="athenacore"
    else
        friendly_name="Lilithos-server"
        service_name="lilithos"
    fi
    
    echo "\nRestarting $friendly_name service..."
    public_ip=$(aws ec2 describe-instances \
        --instance-ids "$instance_id" \
        --query 'Reservations[0].Instances[0].PublicIpAddress' \
        --output text)
    
    ssh -i "$HOME/.ssh/${service_name}-key-new.pem" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "sudo systemctl restart $service_name"
    
    echo "$friendly_name service restarted!"
done

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
