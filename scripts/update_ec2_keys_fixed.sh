#!/bin/bash

# Function to generate .pub file from private key
generate_pub_key() {
    local private_key="$1"
    local pub_key="${private_key}.pub"
    
    if [ ! -f "$private_key" ]; then
        echo "Error: Private key file $private_key not found"
        return 1
    fi
    
    echo "Generating public key for $private_key..."
    ssh-keygen -y -f "$private_key" > "$pub_key"
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to generate public key for $private_key"
        return 1
    fi
    
    echo "Generated public key: $pub_key"
    return 0
}

# Function to update authorized_keys on an EC2 instance using EC2 Instance Connect
update_authorized_keys() {
    local instance_id="$1"
    local key_file="$2"
    local username="ec2-user"  # Default username for Amazon Linux 2
    local pub_key="${key_file}.pub"
    
    echo "Updating authorized_keys for instance: $instance_id"
    
    # Generate the public key if it doesn't exist
    if [ ! -f "$pub_key" ]; then
        if ! generate_pub_key "$key_file"; then
            echo "Error: Failed to generate public key for $key_file"
            return 1
        fi
    fi
    
    # Get the public IP of the instance
    local public_ip=$(aws ec2 describe-instances \
        --instance-ids "$instance_id" \
        --query 'Reservations[0].Instances[0].PublicIpAddress' \
        --output text)
    
    if [ -z "$public_ip" ] || [ "$public_ip" = "None" ]; then
        echo "Error: Could not get public IP for instance $instance_id"
        return 1
    fi
    
    echo "Instance $instance_id has public IP: $public_ip"
    
    # Get the public key content
    local public_key=$(cat "$pub_key")
    
    # Create a temporary script to run on the instance
    local temp_script=$(mktemp)
    cat > "$temp_script" << 'EOF'
#!/bin/bash
# This script will be executed on the remote instance

# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add the new public key to authorized_keys
echo "$PUBLIC_KEY" > ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

echo "Successfully updated authorized_keys on $(hostname)"
echo "New authorized_keys content:"
cat ~/.ssh/authorized_keys
EOF
    
    # Send the public key to the instance using EC2 Instance Connect
    echo "Sending public key to instance $instance_id..."
    
    # Get the availability zone of the instance
    local az=$(aws ec2 describe-instances \
        --instance-ids "$instance_id" \
        --query 'Reservations[0].Instances[0].Placement.AvailabilityZone' \
        --output text)
    
    if [ -z "$az" ]; then
        echo "Error: Could not get availability zone for instance $instance_id"
        rm -f "$temp_script"
        return 1
    fi
    
    # Send the public key to the instance
    if ! aws ec2-instance-connect send-ssh-public-key \
        --instance-id "$instance_id" \
        --availability-zone "$az" \
        --instance-os-user "$username" \
        --ssh-public-key "file://$pub_key"; then
        echo "Error: Failed to send SSH public key to instance $instance_id"
        rm -f "$temp_script"
        return 1
    fi
    
    # Execute the script on the instance
    echo "Executing update script on instance..."
    if ! ssh -i "$key_file" -o StrictHostKeyChecking=no "$username@$public_ip" "PUBLIC_KEY='$public_key' bash -s" < "$temp_script"; then
        echo "Error: Failed to execute script on instance $instance_id"
        rm -f "$temp_script"
        return 1
    fi
    
    # Clean up
    rm -f "$temp_script"
    
    echo "Successfully updated authorized_keys for instance $instance_id"
    return 0
}

# Main script
echo "Starting EC2 key update process..."

# Update AthenaCore-Server (i-01f16ff979f0934b1)
echo -e "\n=== Updating AthenaCore-Server ==="
update_authorized_keys "i-01f16ff979f0934b1" "$HOME/.ssh/serafina-key-new.pem"

# Update Lilithos-server (i-06d885a2cfb302317)
echo -e "\n=== Updating Lilithos-server ==="
update_authorized_keys "i-06d885a2cfb302317" "$HOME/.ssh/lilithos-key-new.pem"

echo -e "\nKey update process completed!"
