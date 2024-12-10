import os
import re

def update_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Debugging print
    print(f"Processing {file_path}")
    
    # Replace relative links in href attributes
    # Exclude absolute URLs, anchor links, and data URIs
    content = re.sub(
        r'(href=")(?!#|https?://|data:)([^"]+)"', 
        lambda m: f'{m.group(1)}/{m.group(2)}"', 
        content
    )
    
    # Replace relative links in src attributes
    # Exclude absolute URLs, anchor links, and data URIs
    content = re.sub(
        r'(src=")(?!#|https?://|data:)([^"]+)"', 
        lambda m: f'{m.group(1)}/{m.group(2)}"', 
        content
    )
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # HTML files to process
    html_files = [
        'dis5.html', 'dis6.html', 'dis7.html', 'dis8.html', 
        'dis9.html', 'index.html', 'nav.html'
    ]
    
    # Process each file
    for filename in html_files:
        file_path = os.path.join(script_dir, filename)
        if os.path.exists(file_path):
            update_links(file_path)
        else:
            print(f"File not found: {file_path}")

if __name__ == '__main__':
    main()
