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
            
            # Remove border-bottom from header css
            # Matches header { ... border-bottom: ... ; ... }
            # Wait, easier way is to just target header CSS block and remove border-bottom line
            def remove_border_from_header(match):
                block = match.group(0)
                # Remove border-bottom:...;
                block = re.sub(r'border-bottom\s*:\s*[^;]+;', '', block)
                return block
                
            new_content = re.sub(r'header\s*\{[^}]+\}', remove_border_from_header, content)
            
            # Let's also remove border-b and border classes from <header ...> tag just in case
            new_content = re.sub(r'<header[^>]+>', lambda m: m.group(0).replace('border-b', '').replace('border ', ''), new_content)
            
            if content != new_content:
                with open(path, 'w') as file:
                    file.write(new_content)
                print(f"Updated {f}")
