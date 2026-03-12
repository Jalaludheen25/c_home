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
            
            # 1. Replace logo.jpeg with logo.png globally
            new_content = content.replace("logo.jpeg", "logo.png")
            
            # Change background color in headers
            new_content = re.sub(
                r'(/\*\s*Header\s*\*/\s*header\s*\{\s*background:\s*)[^;]+;', 
                r'\1#a3f0b1;', 
                new_content
            )
            # Also handle inline styles or different spacing if needed:
            new_content = re.sub(
                r'(?<=header\{background:).*?(?=;)', 
                r'#a3f0b1', 
                new_content
            )
            
            # 2. Modify header logo
            # It usually looks like this:
            # <div class="w-9 h-9 rounded-xl overflow-hidden shadow-sm"><img src="logo.png" alt="Clothyhome"
            #    class="w-full h-full object-cover" /></div>
            # <span class="brand text-xl font-black text-white">Clothyhome</span>
            
            pattern_header = re.compile(
                r'<div class="w-9 h-9 rounded-xl overflow-hidden(?: shadow-sm)?">\s*<img src="logo\.png" alt="Clothyhome"[\s\S]*?class="w-full h-full object-cover"\s*/>\s*</div>\s*<span class="brand[^>]*">Clothyhome</span>'
            )
            
            replacement_header = r'<div class="h-10 md:h-12 overflow-hidden flex items-center">\n                    <img src="logo.png" alt="Clothyhome" class="h-full w-auto object-contain" />\n                </div>'
            
            new_content = pattern_header.sub(replacement_header, new_content)
            
            # 3. Modify footer logo
            # <div class="w-8 h-8 rounded-xl overflow-hidden"><img src="logo.jpeg"
            #        class="w-full h-full object-cover" /></div>
            # <span class="brand text-white text-lg font-black">Clothyhome</span>
            pattern_footer = re.compile(
                r'<div class="w-8 h-8 rounded-xl overflow-hidden(?: shadow-sm)?">\s*<img src="logo\.png"[\s\S]*?class="w-full h-full object-cover"\s*/>\s*</div>\s*<span class="brand[^>]*">Clothyhome</span>'
            )
            
            replacement_footer = r'<div class="h-8 overflow-hidden flex items-center">\n                    <img src="logo.png" alt="Clothyhome" class="h-full w-auto object-contain" />\n                </div>'
            
            new_content = pattern_footer.sub(replacement_footer, new_content)
            
            # 4. Modify login/register large logos
            # <div class="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-3 overflow-hidden shadow-md">
            # <img src="logo.png" alt="Logo" class="w-full h-full object-cover" />
            
            pattern_large = re.compile(
                r'<div[^>]*class="w-16 h-16[^"]*"[^>]*>\s*<img src="logo\.png"[^>]*class="w-full h-full object-cover"[^>]*>\s*</div>'
            )
            
            replacement_large = r'<div class="h-16 mx-auto mb-3 flex items-center justify-center overflow-hidden">\n                    <img src="logo.png" alt="Logo" class="h-full w-auto object-contain" />\n                </div>'
            
            new_content = pattern_large.sub(replacement_large, new_content)
            
            # Also login.html has mx-auto and shadow-md but wait, I just replaced the outer div wrapper class above.
            # Let's verify we replaced all logo.jpegs
            if content != new_content:
                with open(path, 'w') as file:
                    file.write(new_content)
                print(f"Updated {f}")
