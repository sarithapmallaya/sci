import os
import re
import json

def process_folder():
    target_dir = 'json'
    all_cases = []
    
    if not os.path.exists(target_dir):
        print(f"Error: {target_dir} folder not found.")
        return

    # 1. Regex for Petitioner vs Respondent 
    # This captures text before and after "Versus" or "vs"
    # Matches: [1. Case Name Versus Other Name] or [Case Name vs. Other Name]
    case_regex = r'(?:[\d\.]+\s+)?(.*?)\s+(?:Versus|vs\.?|V/s)\s+(.*?)(?=\s+\d{4}\s+INSC|$)'
    
    # 2. Regex for INSC Citation
    insc_regex = r'(\d{4}\s+INSC\s+\d+)'

    for filename in os.listdir(target_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(target_dir, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # We find all INSC citations first to use as anchors
                citations = re.findall(insc_regex, content)
                
                # Split content by citation to isolate each case block
                # This ensures Petitioner/Respondent belong to the correct INSC code
                blocks = re.split(insc_regex, content)
                
                # The split creates: [Text Before Cit1, Cit1, Text Before Cit2, Cit2...]
                # We iterate through the pairs
                for i in range(0, len(citations)):
                    block_text = blocks[i*2].strip()
                    citation = citations[i]
                    
                    # Search for parties in the text block preceding the citation
                    party_match = re.search(r'(?:^|\n)(?:[\d\.]+\s+)?(.*?)\s+(?:Versus|vs\.?|V/s)\s+(.*)', block_text, re.IGNORECASE)
                    
                    if party_match:
                        all_cases.append({
                            "petitioner": party_match.group(1).strip('# \n').strip(),
                            "respondent": party_match.group(2).strip().split('\n')[0].strip(),
                            "insc_citation": citation
                        })

    # Save the full list to one file
    output_file = os.path.join(target_dir, 'all_cases.json')
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(all_cases, out_f, indent=4)
    
    print(f"Done! Found {len(all_cases)} cases in {filename}")

if __name__ == "__main__":
    process_folder()
