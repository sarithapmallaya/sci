import os
import re
import json

def process_folder():
    target_dir = 'json'
    
    # Check if directory exists
    if not os.path.exists(target_dir):
        print(f"Directory {target_dir} not found.")
        return

    for filename in os.listdir(target_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(target_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Regex for Petitioner vs Respondent
                # Looks for: Party A (Versus/vs) Party B
                title_match = re.search(r'(.*?)\s+(?:Versus|vs\.?|V/s)\s+(.*)', content, re.IGNORECASE)
                
                # Regex for INSC Citation: e.g., 2024 INSC 123
                insc_match = re.search(r'(\d{4}\s+INSC\s+\d+)', content)
                
                data = {
                    "petitioner": title_match.group(1).strip('# ').strip() if title_match else "Unknown",
                    "respondent": title_match.group(2).strip().split('\n')[0] if title_match else "Unknown",
                    "insc_citation": insc_match.group(1) if insc_match else "N/A"
                }
                
                # Save as [filename].json in the same folder
                output_path = file_path.replace('.md', '.json')
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    json.dump(data, out_f, indent=4)
                print(f"Processed: {filename}")

if __name__ == "__main__":
    process_folder()
