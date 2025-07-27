#!/bin/bash

# Function to deploy fix and restart service on an EC2 instance
deploy_fix_and_restart() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Deploying fix and restarting service on $friendly_name ($instance_id) ==="
    
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
    
    # Create a temporary directory for the fix
    local temp_dir=$(mktemp -d)
    
    # Create the target directory structure
    mkdir -p "$temp_dir/athenamist_integration/core"
    
    # Copy the fixed file to the temporary directory with the correct path
    cp athenamist_integration/core/sam_integration.py "$temp_dir/athenamist_integration/core/"
    
    # Create a script to deploy the fix and restart the service
    local deploy_script="$temp_dir/deploy_fix.sh"
    cat > "$deploy_script" << 'EOF'
#!/bin/bash

# Exit on error
set -e

echo "Deploying fixed sam_integration.py..."

# Go to the project directory
cd /home/ec2-user/Primal-Genesis-Engine-Sovereign

# Backup the original file
if [ -f "athenamist_integration/core/sam_integration.py" ]; then
    sudo cp athenamist_integration/core/sam_integration.py athenamist_integration/core/sam_integration.py.bak
    echo "Backup created at athenamist_integration/core/sam_integration.py.bak"
else
    echo "Original file not found, no backup created."
fi

# Copy the fixed file
echo "Copying fixed file..."
sudo cp -r /tmp/fix/athenamist_integration ./

# Fix permissions
sudo chown -R ec2-user:ec2-user athenamist_integration

# Get the service name from the current directory
SERVICE_NAME="$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr -d '-_')"

# Restart the service
echo "Restarting $SERVICE_NAME service..."
sudo systemctl restart $SERVICE_NAME

echo "$SERVICE_NAME service restarted!"

echo "Verifying service status..."
sudo systemctl status $SERVICE_NAME --no-pager

echo "Deployment and service restart complete!"
EOF
    
    # Make the deploy script executable
    chmod +x "$deploy_script"
    
    # Copy the fix directory to the instance's /tmp
    echo "Copying fix directory to $friendly_name..."
    scp -i "$ssh_key" -o StrictHostKeyChecking=no -r "$temp_dir/" "ec2-user@$public_ip:/tmp/fix/"
    
    # Copy the deploy script to the instance
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$deploy_script" "ec2-user@$public_ip:~/deploy_fix.sh"
    
    # Make the deploy script executable
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "chmod +x ~/deploy_fix.sh"
    
    # Execute the deploy script on the instance
    echo "Running deploy script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "~/deploy_fix.sh"
    
    # Clean up
    rm -rf "$temp_dir"
    
    echo "\nFix deployed and service restarted on $friendly_name!"
}

# Main script
echo "Starting deployment of fix and service restart on all servers..."

# Deploy fix and restart AthenaCore-Server
echo "\n===== Deploying fix to AthenaCore-Server ====="
deploy_fix_and_restart "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Deploy fix and restart Lilithos-server
echo "\n===== Deploying fix to Lilithos-server ====="
deploy_fix_and_restart "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nFix deployment and service restart complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
