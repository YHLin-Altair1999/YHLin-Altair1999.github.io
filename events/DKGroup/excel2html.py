'''
Convert the data in xlsx into a HTML table format that can be directly embedded into the DKGroup website. The first tab is treated as the latest and is fully expanded, while subsequent tabs are wrapped in collapsible containers to keep the page organized. 
'''

import openpyxl
from html import escape

def excel_to_html(excel_fname, index_fname):
    # Load the workbook
    wb = openpyxl.load_workbook(excel_fname)
    
    full_html_content = ""

    # Loop through each tab (sheet) in the Excel file
    for index, ws in enumerate(wb.worksheets):
        sheet_name = ws.title  # e.g., "Spring 2026", "Winter 2026"
        is_latest = (index == 0) # The first tab is treated as the latest

        # Read rows and skip the header row
        rows = list(ws.iter_rows(values_only=True))
        if not rows or len(rows) <= 1:
            # Skip empty sheets or sheets that only have a header
            continue
        
        data_rows = rows[1:]
        table_rows_html = ""

        # Iterate through the data rows in the current sheet
        for row in data_rows:
            if not any(row):
                continue
                
            # Pad row to ensure 5 elements [Date, Author/Year, Title, Presenter, Notes, URL]
            padded_row = list(row) + [""] * (5 - len(row))
            
            date_val = padded_row[0]
            if hasattr(date_val, 'strftime'):  # datetime object
                date = date_val.strftime('%Y-%m-%d')
            else:
                date = escape(str(date_val or ""))  # use the YYYY-MM-DD format, not time info.
            author_year = escape(str(padded_row[1] or ""))
            title = escape(str(padded_row[2] or ""))
            presenter = escape(str(padded_row[3] or ""))
            url = str(padded_row[5] or "").strip()
            notes = escape(str(padded_row[4] or "")) if len(padded_row) > 5 else ""

            # Handle linking Author & Year to the URL
            if url:
                author_cell = f'<td><a href="{escape(url)}">{author_year}</a></td>'
            else:
                author_cell = f'<td>{author_year}</td>'

            table_rows_html += '                                        <tr>\n'
            table_rows_html += f'                                            <td>{date}</td>\n'
            table_rows_html += f'                                            {author_cell}\n'
            table_rows_html += f'                                            <td>{title}</td>\n'
            table_rows_html += f'                                            <td>{presenter}</td>\n'
            table_rows_html += f'                                            <td>{notes}</td>\n'
            table_rows_html += '                                        </tr>\n'

        # Generate the framework for this specific sheet's table
        sheet_html = f'                            <h2>{escape(sheet_name)}</h2>\n'
        sheet_html += '                            <div class="table-wrapper">\n'
        sheet_html += '                                <table class="alt">\n'
        sheet_html += '                                    <thead>\n'
        sheet_html += '                                        <tr>\n'
        sheet_html += '                                            <th width=100pt>Date</th>\n'
        sheet_html += '                                            <th width="20%">Author & Year</th>\n'
        sheet_html += '                                            <th>Title</th>\n'
        sheet_html += '                                            <th width="15%">Presenter</th>\n'
        sheet_html += '                                            <th>Notes</th>\n'
        sheet_html += '                                        </tr>\n'
        sheet_html += '                                    </thead>\n'
        sheet_html += '                                    <tbody>\n'
        sheet_html += table_rows_html
        sheet_html += '                                    </tbody>\n'
        sheet_html += '                                </table>\n'
        sheet_html += '                            </div>\n'

        # If it's NOT the first tab, wrap the entire block in a collapsible container
        if not is_latest:
            sheet_html = (
                f'                            <details>\n'
                f'                                <summary>{escape(sheet_name.replace('_', ' '))} (Click to expand)</summary>\n'
                f'{sheet_html}'
                f'                            </details>\n'
            )

        full_html_content += sheet_html + "\n"

    # Inject into index.html
    with open(index_fname, 'r', encoding='utf-8') as f:
        html = f.read()

    start_tag = '<!-- TABLE_START -->'
    end_tag = '<!-- TABLE_END -->'

    if start_tag in html and end_tag in html:
        parts = html.split(start_tag)
        before = parts[0]
        after = parts[1].split(end_tag)[1]
        
        new_html = f'{before}{start_tag}\n{full_html_content}\n                            {end_tag}{after}'
        
        with open(index_fname, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("Successfully updated the table in index.html.")
    else:
        print("Error: Could not find the START and END tags in index.html.")

if __name__ == "__main__":
    excel_fname = './PaperDiscussionRecord.xlsx'
    index_fname = './index.html'
    excel_to_html(excel_fname, index_fname)