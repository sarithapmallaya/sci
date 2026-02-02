import os
import re
import json

def process_folder():
    target_dir = 'json'
    all_cases = []
    
    if not os.path.exists(target_dir):
        return

    for filename in sorted(os.listdir(target_dir)):
        if filename.endswith('.md'):
            file_path = os.path.join(target_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                for line in lines:
                    # Only process lines that look like table rows (contain multiple pipes)
                    if line.count('|') >= 3:
                        # Split by pipe and clean whitespace
                        columns = [col.strip() for col in line.split('|')]
                        
                        # Markdown tables often have empty strings at the start/end due to leading/trailing pipes
                        columns = [c for c in columns if c != '']
                        
                        # Skip header rows or separator rows (---)
                        if not columns or "Petitioner" in columns[0] or "---" in columns[0]:
                            continue
                            
                        # Extract data from the row
                        # 1. Case Name: From the column (usually the 1st or 2nd)
                        # 2. Link: Look for (...) inside that column or a dedicated link column
                        # 3. Citation: Look for "2026 INSC ..."
                        
                        row_text = " ".join(columns)
                        
                        name_match = re.search(r'\[([^\]]+)\]', row_text)
                        link_match = re.search(r'\((https?://[^\)]+)\)', row_text)
                        cite_match = re.search(r'(\d{4}\s+INSC\s+\d+)', row_text)
                        
                        if name_match and cite_match:
                            all_cases.append({
                                "case_name": name_match.group(1).replace('**', '').strip(),
                                "link": link_match.group(1) if link_match else "N/A",
                                "citation": cite_match.group(1)
                            })

    # Save to json/all_cases.json
    output_path = os.path.join(target_dir, 'all_cases.json')
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(all_cases, out_f, indent=4)
    
    print(f"Successfully parsed {len(all_cases)} rows from the table.")

if __name__ == "__main__":
    process_folder()
