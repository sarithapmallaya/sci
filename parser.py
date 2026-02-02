import os
import re
import json

def process_folder():
    target_dir = 'json'
    all_cases = []
    
    if not os.path.exists(target_dir):
        return

    # Pattern explanation:
    # 1. \[(.*?)\] -> Captures the Case Name inside square brackets
    # 2. \((.*?)\) -> Captures the URL inside parentheses
    # 3. (202\d\s+INSC\s+\d+) -> Captures the Neutral Citation
    case_pattern = r'\[(.*?)\]\((.*?)\).*?(202\d\s+INSC\s+\d+)'

    for filename in os.listdir(target_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(target_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # findall finds every occurrence in the file
                matches = re.findall(case_pattern, content, re.DOTALL)
                
                for match in matches:
                    case_name = match[0].strip()
                    url = match[1].strip()
                    citation = match[2].strip()
                    
                    all_cases.append({
                        "case_name": case_name,
                        "citation": citation,
                        "link": url
                    })

    # Save to all_cases.json
    output_path = os.path.join(target_dir, 'all_cases.json')
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(all_cases, out_f, indent=4)
    
    print(f"Successfully extracted {len(all_cases)} cases with links.")

if __name__ == "__main__":
    process_folder()
