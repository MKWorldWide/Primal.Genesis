#!/bin/bash

# Function to fix sam_integration.py on a remote server
fix_remote_sam_integration() {
    local instance_id="$1"
    local ssh_key="$2"
    local friendly_name="$3"
    
    echo "\n=== Fixing sam_integration.py on $friendly_name ($instance_id) ==="
    
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
    local fix_script="$temp_dir/fix_sam.sh"
    cat > "$fix_script" << 'EOF'
#!/bin/bash

# Exit on error
set -e

echo "Fixing sam_integration.py..."

# Go to the project directory
cd /home/ec2-user/Primal-Genesis-Engine-Sovereign

# Path to the sam_integration.py file
SAM_FILE="athenamist_integration/core/sam_integration.py"

# Backup the original file
if [ -f "$SAM_FILE" ]; then
    # Create a backup
    sudo cp "$SAM_FILE" "${SAM_FILE}.bak"
    echo "Backup created at ${SAM_FILE}.bak"
    
    # Fix the file using sed with proper escaping
    echo "Applying fix to $SAM_FILE..."
    
    # First, fix the indentation issue by replacing the problematic section
    # with the correct indentation and syntax
    sudo sed -i '369s/.*/        # Generate cache key for this search/; \
    370s/.*/        search_params = {/; \
    371s/.*/            \x27term\x27: search_term,/; \
    372s/.*/            \x27type\x27: entity_type,/; \
    373s/.*/            \x27status\x27: registration_status,/; \
    374s/.*/            \x27limit\x27: limit/; \
    375s/.*/        }/; \
    376s/.*/        cache_key = f\"search_{hash(frozenset(search_params.items()))}\"/' "$SAM_FILE"
    
    # Fix permissions
    sudo chown ec2-user:ec2-user "$SAM_FILE"
    
    echo "Fix applied to $SAM_FILE"
    
    # Get the service name from the current directory
    SERVICE_NAME="$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr -d '-_')"
    
    # Restart the service
    echo "Restarting $SERVICE_NAME service..."
    sudo systemctl restart "$SERVICE_NAME"
    
    echo "$SERVICE_NAME service restarted!"
    
    # Verify the service status
    echo "Verifying service status..."
    sudo systemctl status "$SERVICE_NAME" --no-pager
    
    # Check if the service is running
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo "✅ $SERVICE_NAME is running!"
    else
        echo "❌ $SERVICE_NAME failed to start. Check the logs with: sudo journalctl -u $SERVICE_NAME -n 50"
    fi
else
    echo "Error: $SAM_FILE not found"
    exit 1
fi

echo "Fix and service restart complete!"
EOF
    
    # Make the fix script executable
    chmod +x "$fix_script"
    
    # Copy the fix script to the instance
    echo "Copying fix script to $friendly_name..."
    scp -i "$ssh_key" -o StrictHostKeyChecking=no "$fix_script" "ec2-user@$public_ip:~/fix_sam.sh"
    
    # Make the fix script executable on the remote server
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "chmod +x ~/fix_sam.sh"
    
    # Execute the fix script on the instance
    echo "Running fix script on $friendly_name..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" "~/fix_sam.sh"
    
    # Clean up
    rm -rf "$temp_dir"
    
    echo "\nFix applied and service restarted on $friendly_name!"
}

# Main script
echo "Starting direct fix for sam_integration.py on all servers..."

# Fix AthenaCore-Server
echo "\n===== Fixing AthenaCore-Server ====="
fix_remote_sam_integration "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" "AthenaCore-Server"

# Fix Lilithos-server
echo "\n===== Fixing Lilithos-server ====="
fix_remote_sam_integration "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" "Lilithos-server"

echo "\nFix deployment complete on all servers!"

echo "\nVerifying services..."

# Verify the services
./scripts/verify_deployment.sh

echo "\nAll done! Review the output above to ensure both services are running correctly."
