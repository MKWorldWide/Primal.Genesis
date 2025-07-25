#!/bin/bash

# Function to check service status on an EC2 instance
check_service() {
    local instance_id="$1"
    local ssh_key="$2"
    local service_name="$3"
    local friendly_name="$4"
    
    echo "\n=== Checking $friendly_name ($instance_id) ==="
    
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
    
    # Check service status
    echo "Checking $service_name service status..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "systemctl status $service_name --no-pager | head -n 5"
    
    # Check if service is listening on port 8000
    echo "\nChecking if service is listening on port 8000..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "sudo netstat -tuln | grep ':8000' || echo 'Not listening on port 8000'"
    
    # Check service logs
    echo "\nRecent service logs:"
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "sudo journalctl -u $service_name --no-pager | tail -n 10"
    
    echo "\n$friendly_name verification complete!"
    echo "You can access $friendly_name at: http://$public_ip:8000"
}

# Main script
echo "Starting deployment verification..."

# Check AthenaCore service
check_service "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" \
    "athenacore" "AthenaCore-Server"

# Check LilithOS service
check_service "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" \
    "lilithos" "Lilithos-server"

echo "\nDeployment verification complete!"
