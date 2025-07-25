"""
This script is used to fix the sam_integration.py file on remote EC2 instances.
It should be copied to the remote server and executed there.
"""

def fix_sam_integration(file_path):
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the line with the cache key generation
    for i, line in enumerate(lines):
        if 'cache_key = f"search_{hash(frozenset(' in line:
            start_line = i - 1  # The line before the cache key generation
            
            # Replace the problematic section with the fixed version
            fixed_lines = [
                '        # Generate cache key for this search\n',
                '        search_params = {\n',
                "            'term': search_term,\n",
                "            'type': entity_type,\n",
                "            'status': registration_status,\n",
                "            'limit': limit\n",
                '        }\n',
                '        cache_key = f"search_{hash(frozenset(search_params.items()))}"\n'
            ]
            
            # Replace the problematic lines with the fixed version
            lines = lines[:start_line] + fixed_lines + lines[i+8:]
            break
    
    # Write the fixed file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"Successfully fixed {file_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python fix_sam_integration.py <path_to_sam_integration.py>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    fix_sam_integration(file_path)
