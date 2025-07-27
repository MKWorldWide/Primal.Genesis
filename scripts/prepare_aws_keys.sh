#!/bin/bash

# Function to prepare a key for AWS import
prepare_key() {
    local key_name=$1
    local key_file=~/.ssh/$key_name.pub
    local output_file=~/.ssh/${key_name}_aws.pub
    
    # Extract the key type and actual key
    local key_type key_content
    key_type=$(awk '{print $1}' "$key_file")
    key_content=$(awk '{print $2}' "$key_file")
    
    # Create the AWS format
    echo "$key_type $key_content $key_name" > "$output_file"
    
    # Convert to base64
    openssl base64 -in "$output_file" -out "${output_file}.b64"
    echo "Prepared $key_name for AWS import"
    echo "Base64 encoded key saved to ${output_file}.b64"
}

# Prepare both keys
prepare_key "serafina-key"
prepare_key "lilithos-key"

echo "\nTo import a key to AWS, use:"
echo "aws ec2 import-key-pair --key-name 'KEY_NAME' --public-key-material fileb://~/.ssh/KEY_NAME_aws.pub.b64"
