import pandas as pd
from bs4 import BeautifulSoup
import glob
import os

def extract_case_details():
    # Detect any HTML file in the root directory
    html_files = glob.glob("*.html")
    if not html_files:
        print("No HTML file found.")
        return
    
    html_path = html_files[0]
    print(f"Processing: {html_path}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    # Find the case data table (ignoring layout/calendar tables) [cite: 3, 6, 9]
    target_table = None
    for table in soup.find_all('table'):
        header_text = table.get_text().lower()
        if "diary number" in header_text or "case number" in header_text:
            target_table = table
            break

    if not target_table:
        print("Case data table not found.")
        return

    data = []
    rows = target_table.find_all('tr')
    
    for row in rows:
        cols = row.find_all(['td', 'th'])
        if len(cols) < 5: # Filters out non-data rows [cite: 2, 5]
            continue
            
        row_data = []
        for col in cols:
            link = col.find('a')
            cell_text = col.get_text(separator=" ", strip=True)
            
            # Preserve PDF links attached to Neutral Citations 
            if link and link.get('href'):
                url = link['href']
                if not url.startswith('http'):
                    url = "https://www.sci.gov.in" + url
                row_data.append(f"[{cell_text}]({url})")
            else:
                row_data.append(cell_text)
        data.append(row_data)

    if data:
        # Use first row as headers (Serial Number, Diary Number, Case Number, etc.) [cite: 2, 5]
        df = pd.DataFrame(data[1:], columns=data[0])
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("# Supreme Court Judgments\n\n")
            f.write("Note: Neutral Citations in the **Judgment** column link directly to official PDFs. [cite: 2, 8]\n\n")
            f.write(df.to_markdown(index=False))
        print("README.md updated successfully.")

if __name__ == "__main__":
    extract_case_details()
