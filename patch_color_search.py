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
            # from `header { background: #51ed6d;` to `#e1f2e4;`
            new_content = re.sub(
                r'(header\s*\{\s*background\s*:\s*)[^;]+(;)', 
                r'\g<1>#e1f2e4\g<2>', 
                content
            )
            
            # Since the user wants the search box, in index.html desktop:
            # background:#24382a; -> background:#e1f2e4;
            # and products.html desktop:
            # background:#f7f8fa; -> background:#e1f2e4;
            # For the mobile ones: they might not have background style. Let's add it if not present,
            # or replace if present.
            
            # Let's target the search inputs specifically by x-model="searchQuery" style attributes.
            # Example desktop: style="border-color:#2d4533;font-family:Poppins,sans-serif;background:#24382a;"
            # Example mobile: style="border-color:#dde8e3;font-family:Poppins,sans-serif;"
            
            def replace_search_bg(match):
                attr = match.group(0)
                if ';background:' in attr:
                    # replace the background value
                    return re.sub(r'(;background:)[^;"]+', r'\g<1>#e1f2e4', attr)
                else:
                    # append the background value before the closing quote
                    return attr[:-1] + ';background:#e1f2e4;"'
            
            # match style="..." inside <input type="text" x-model="searchQuery" tags
            # We'll use a larger regex up to style
            new_content = re.sub(
                r'<input[^>]+x-model="searchQuery"[^>]+style="[^"]+"',
                lambda m: re.sub(r'style="[^"]+"', replace_search_bg, m.group(0)),
                new_content
            )
            
            if content != new_content:
                with open(path, 'w') as file:
                    file.write(new_content)
                print(f"Updated {f}")
