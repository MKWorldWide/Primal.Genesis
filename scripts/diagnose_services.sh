#!/bin/bash

# Function to diagnose service on an EC2 instance
diagnose_service() {
    local instance_id="$1"
    local ssh_key="$2"
    local service_name="$3"
    local friendly_name="$4"
    
    echo "\n=== Diagnosing $friendly_name ($instance_id) ==="
    
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
    
    # Check if the application directory exists
    echo "\nChecking application directory structure..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "ls -la ~/Primal-Genesis-Engine-Sovereign/ 2>/dev/null || echo 'Application directory not found'"
    
    # Check for Python modules
    echo "\nChecking Python modules..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "ls -la ~/Primal-Genesis-Engine-Sovereign/athenacore/ 2>/dev/null || echo 'AthenaCore module not found'"
    
    # Check service file
    echo "\nChecking service file..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "sudo cat /etc/systemd/system/${service_name}.service 2>/dev/null || echo 'Service file not found'"
    
    # Check systemd status
    echo "\nChecking systemd status..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "sudo systemctl list-units --type=service | grep -i $service_name || echo 'Service not found in systemd'"
    
    # Check application logs
    echo "\nChecking application logs..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "ls -la /var/log/ | grep -i $service_name || echo 'No application logs found'"
    
    # Check Python version
    echo "\nChecking Python version..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "python3 --version && echo 'Python path:' && which python3"
    
    # Check installed Python packages
    echo "\nChecking installed Python packages..."
    ssh -i "$ssh_key" -o StrictHostKeyChecking=no "ec2-user@$public_ip" \
        "pip3 list | grep -E 'flask|gunicorn|requests' || echo 'No relevant Python packages found'"
    
    echo "\n$friendly_name diagnosis complete!"
}

# Main script
echo "Starting service diagnosis..."

# Diagnose AthenaCore service
echo "\n===== Diagnosing AthenaCore-Server ====="
diagnose_service "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem" \
    "athenacore" "AthenaCore-Server"

# Diagnose LilithOS service
echo "\n===== Diagnosing Lilithos-server ====="
diagnose_service "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem" \
    "lilithos" "Lilithos-server"

echo "\nDiagnosis complete! Review the output above to identify any issues."
