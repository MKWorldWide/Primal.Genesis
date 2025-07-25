#!/bin/bash

# Function to perform detailed service diagnosis
diagnose_service_detailed() {
    local instance_id="$1"
    local ssh_key="$2"
    local service_name="$3"
    local friendly_name="$4"
    
    echo "\n=== Detailed Diagnosis for $friendly_name ($instance_id) ==="
    
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
    
    # Check if systemd is available
    echo "\n1. Checking systemd status..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "systemctl --version || echo 'systemd not available'"
    
    # Check service file existence and content
    echo "\n2. Checking service file..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "ls -la /etc/systemd/system/ | grep -i $service_name || echo 'No service file found'"
    
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "sudo cat /etc/systemd/system/${service_name}.service 2>/dev/null || echo 'Could not read service file'"
    
    # Check service status
    echo "\n3. Checking service status..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "sudo systemctl status ${service_name} --no-pager || echo 'Service status check failed'"
    
    # Check journal logs for the service
    echo "\n4. Checking journal logs..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "sudo journalctl -u ${service_name} --no-pager -n 20 2>/dev/null || echo 'No journal logs available'"
    
    # Check application directory and permissions
    echo "\n5. Checking application directory..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "ls -la ~/Primal-Genesis-Engine-Sovereign/ 2>/dev/null || echo 'Application directory not found'"
    
    # Check Python environment
    echo "\n6. Checking Python environment..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "which python3 && python3 --version && pip3 --version || echo 'Python/pip not found'"
    
    # Check running processes
    echo "\n7. Checking running processes..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "ps aux | grep -i python || echo 'No Python processes found'"
    
    # Check network connectivity
    echo "\n8. Checking network connectivity..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "netstat -tuln | grep -E ':8000|:80' || echo 'No services listening on port 8000 or 80'"
    
    echo "\n=== End of detailed diagnosis for $friendly_name ==="
}

# Main script
echo "Starting detailed service diagnosis..."

# Diagnose AthenaCore-Server
echo "\n===== Detailed Diagnosis for AthenaCore-Server ====="
diagnose_service_detailed "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" \
    "athenacore" "AthenaCore-Server"

# Diagnose Lilithos-server
echo "\n===== Detailed Diagnosis for Lilithos-server ====="
diagnose_service_detailed "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" \
    "lilithos" "Lilithos-server"

echo "\nDiagnosis complete! Review the output above to identify any issues."
