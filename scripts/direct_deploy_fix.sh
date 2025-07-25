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
    
    # Create a temporary file with the fixed content
    local temp_file=$(mktemp)
    cat > "$temp_file" << 'EOF'
    # Generate cache key for this search
    search_params = {
        'term': search_term,
        'type': entity_type,
        'status': registration_status,
        'limit': limit
    }
    cache_key = f"search_{hash(frozenset(search_params.items()))}"
EOF

    # Create a script to deploy the fix and restart the service
    local deploy_script=$(mktemp)
    cat > "$deploy_script" << 'EOF'
#!/bin/bash

# Exit on error
set -e

# Go to the project directory
cd /home/ec2-user/Primal-Genesis-Engine-Sovereign

# Backup the original file
if [ -f "athenamist_integration/core/sam_integration.py" ]; then
    sudo cp athenamist_integration/core/sam_integration.py athenamist_integration/core/sam_integration.py.bak
    echo "Backup created at athenamist_integration/core/sam_integration.py.bak"
    
    # Apply the fix directly
    echo "Applying fix to sam_integration.py..."
    
    # Create a temporary file with the fix
    TMP_FILE=$(mktemp)
    cat > "$TMP_FILE" << 'FIX_EOF'
    # Generate cache key for this search
    search_params = {
        'term': search_term,
        'type': entity_type,
        'status': registration_status,
        'limit': limit
    }
    cache_key = f"search_{hash(frozenset(search_params.items()))}"
FIX_EOF
    
    # Replace the problematic section in the file
    sed -i '369s/.*/    # Generate cache key for this search/' athenamist_integration/core/sam_integration.py
    sed -i '370s/.*/    search_params = {\'$'\n''        \'term\': search_term,\'$'\n''        \'type\': entity_type,\'$'\n''        \'status\': registration_status,\'$'\n''        \'limit\': limit\'$'\n''    }\'$'\n''    cache_key = f\"search_{hash(frozenset(search_params.items()))}\"/' athenamist_integration/core/sam_integration.py
    
    # Remove the temporary file
    rm -f "$TMP_FILE"
    
    echo "Fix applied to sam_integration.py"
    
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
    echo "Error: sam_integration.py not found in the expected location"
    exit 1
fi

echo "Deployment and service restart complete!"
EOF
    
    # Make the deploy script executable
    chmod +x "$deploy_script"
    
    # Copy the deploy script to the instance
    echo "Copying deploy script to $friendly_name..."
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$deploy_script" "ec2-user@$public_ip:~/deploy_fix.sh"
    
    # Execute the deploy script on the instance
    echo "Running deploy script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "chmod +x ~/deploy_fix.sh && ~/deploy_fix.sh"
    
    # Clean up
    rm -f "$temp_file" "$deploy_script"
    
    echo "\nFix deployed and service restarted on $friendly_name!"
}

# Main script
echo "Starting direct deployment of fix to all servers..."

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
