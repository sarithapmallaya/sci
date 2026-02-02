import pandas as pd
from bs4 import BeautifulSoup
import glob
import os
from datetime import datetime

def extract_case_details():
    # Detect all HTML files in the root directory
    html_files = glob.glob("*.html")
    if not html_files:
        print("No HTML files found to process.")
        return

    all_data = []
    headers = []

    for html_path in html_files:
        print(f"Processing file: {html_path}")
        with open(html_path, 'r', encoding='utf-8') as f:
            # Use lxml for fast, robust HTML parsing
            soup = BeautifulSoup(f, 'lxml')

        # Find tables specifically containing "Diary Number" or "Case Number" [cite: 3, 54]
        for table in soup.find_all('table'):
            table_text = table.get_text().lower()
            if "diary number" in table_text or "case number" in table_text:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    # Filter out small layout tables or empty rows
                    if len(cols) < 5:
                        continue
                    
                    row_data = []
                    for col in cols:
                        # Extract the clickable PDF link if it exists
                        link = col.find('a')
                        text = col.get_text(separator=" ", strip=True)
                        
                        if link and link.get('href'):
                            url = link['href']
                            # Ensure link points to the official sci.gov.in API/Server
                            if not url.startswith('http'):
                                url = "https://www.sci.gov.in" + url
                            row_data.append(f"[{text}]({url})")
                        else:
                            row_data.append(text)
                    
                    # Identify and store headers only once
                    if "diary" in str(row_data).lower() and not headers:
                        headers = row_data
                    # Append data rows (skipping the header row if already added)
                    elif "diary" not in str(row_data).lower():
                        all_data.append(row_data)

    if all_data:
        # Convert to DataFrame and remove duplicate rows (if same file uploaded again)
        df = pd.DataFrame(all_data, columns=headers if headers else None)
        df = df.drop_duplicates()
        
        # Add a "Last Updated" timestamp for clarity
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(f"# Supreme Court Judgments - PDF Repository\n\n")
            f.write(f"**Last Sync:** {timestamp} IST\n\n")
            f.write(f"Click the citations in the **Judgment** column to open official PDFs.\n\n")
            f.write(df.to_markdown(index=False))
        print("Successfully merged data and updated README.md")

if __name__ == "__main__":
    extract_case_details()
