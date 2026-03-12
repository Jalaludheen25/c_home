import os
import re

dir_path = "/Users/jalaludheenok/development/Clothyhome"

for root, dirs, files in os.walk(dir_path):
    if "node_modules" in root or ".git" in root:
        continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Change background color in headers
            new_content = re.sub(
                r'(header\s*\{\s*background\s*:\s*)[^;]+(;)', 
                r'\g<1>#51ed6d\g<2>', 
                content
            )
            
            if content != new_content:
                with open(path, 'w') as file:
                    file.write(new_content)
                print(f"Updated {f}")
