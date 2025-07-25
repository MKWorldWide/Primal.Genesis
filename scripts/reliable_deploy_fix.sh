#!/bin/bash

# Function to deploy fix and restart service on an EC2 instance
deploy_fix() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Deploying fix to $friendly_name ($instance_id) ==="
    
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
    
    # Copy the fix script to the temporary directory
    cp scripts/fix_sam_integration.py "$temp_dir/"
    
    # Create a script to deploy the fix and restart the service
    local deploy_script="$temp_dir/deploy_fix.sh"
    cat > "$deploy_script" << 'EOF'
#!/bin/bash

# Exit on error
set -e

echo "Deploying fix to sam_integration.py..."

# Go to the project directory
cd /home/ec2-user/Primal-Genesis-Engine-Sovereign

# Path to the sam_integration.py file
SAM_FILE="athenamist_integration/core/sam_integration.py"

# Backup the original file
if [ -f "$SAM_FILE" ]; then
    sudo cp "$SAM_FILE" "${SAM_FILE}.bak"
    echo "Backup created at ${SAM_FILE}.bak"
    
    # Run the fix script
    echo "Running fix script..."
    python3 fix_sam_integration.py "$SAM_FILE"
    
    # Fix permissions
    sudo chown ec2-user:ec2-user "$SAM_FILE"
    
    # Get the service name from the current directory
    SERVICE_NAME="$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr -d '-_')"
    
    # Restart the service
    echo "Restarting $SERVICE_NAME service..."
    sudo systemctl restart "$SERVICE_NAME"
    
    echo "$SERVICE_NAME service restarted!"
    
    # Verify the service status
    echo "Verifying service status..."
    sudo systemctl status "$SERVICE_NAME" --no-pager
else
    echo "Error: $SAM_FILE not found"
    exit 1
fi

echo "Deployment and service restart complete!"
EOF
    
    # Make the deploy script executable
    chmod +x "$deploy_script"
    
    # Copy the fix script to the instance
    echo "Copying fix script to $friendly_name..."
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$temp_dir/fix_sam_integration.py" "ec2-user@$public_ip:~/"
    
    # Copy the deploy script to the instance
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$deploy_script" "ec2-user@$public_ip:~/deploy_fix.sh"
    
    # Make the deploy script executable on the remote server
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "chmod +x ~/deploy_fix.sh"
    
    # Execute the deploy script on the instance
    echo "Running deploy script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "~/deploy_fix.sh"
    
    # Clean up
    rm -rf "$temp_dir"
    
    echo "\nFix deployed and service restarted on $friendly_name!"
}

# Main script
echo "Starting reliable deployment of fix to all servers..."

# Deploy fix to AthenaCore-Server
echo "\n===== Deploying fix to AthenaCore-Server ====="
deploy_fix "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Deploy fix to Lilithos-server
echo "\n===== Deploying fix to Lilithos-server ====="
deploy_fix "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nFix deployment complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
