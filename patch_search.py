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
            
            def replace_search_bg(match):
                attr = match.group(0)
                if ';background:' in attr:
                    # replace the background value
                    return re.sub(r'(;background:)[^;"]+', r'\g<1>#2596be', attr)
                else:
                    return attr
            
            new_content = re.sub(
                r'<input[^>]+x-model="searchQuery"[^>]+style="[^"]+"',
                lambda m: re.sub(r'style="[^"]+"', replace_search_bg, m.group(0)),
                content
            )
            
            if content != new_content:
                with open(path, 'w') as file:
                    file.write(new_content)
                print(f"Updated {f}")
