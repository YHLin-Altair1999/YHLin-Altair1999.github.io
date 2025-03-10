import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

def get_article_info(article_path):
    """Extract article information from HTML file."""
    with open(article_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        h1 = soup.find('h1')
        title = h1.string if h1 else os.path.basename(article_path)
        return title

def get_articles():
    """Get all articles from the articles directory."""
    articles = []
    articles_dir = "articles"
    
    # Walk through all directories in articles folder
    for root, dirs, files in os.walk(articles_dir):
        for dir in dirs:
            # Skip if directory doesn't match date pattern (YYYYMMDD_*)
            if not re.match(r'\d{8}_', dir):
                continue
                
            # Find main HTML file in directory
            dir_path = os.path.join(root, dir)
            html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]
            
            if html_files:
                date_str = dir[:8]
                date = datetime.strptime(date_str, '%Y%m%d')
                formatted_date = date.strftime('%Y.%m.%d')
                
                article_path = os.path.join(dir_path, html_files[0])
                title = get_article_info(article_path)
                relative_path = os.path.join(dir, html_files[0]).replace('\\', '/')
                
                articles.append({
                    'date': formatted_date,
                    'title': title,
                    'path': relative_path
                })
    
    return sorted(articles, key=lambda x: x['date'], reverse=True)

def update_index_html():
    """Update the index.html file with article entries."""
    index_path = "articles/index.html"
    
    with open(index_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Find the table body
    tbody = soup.find('tbody')
    if not tbody:
        return
    
    # Clear existing entries
    tbody.clear()
    
    # Add new entries
    articles = get_articles()
    for article in articles:
        tr = soup.new_tag('tr')
        
        td_date = soup.new_tag('td')
        td_date.string = article['date']
        tr.append(td_date)
        
        td_topic = soup.new_tag('td')
        a = soup.new_tag('a', href=article['path'])
        a.string = article['title']
        td_topic.append(a)
        tr.append(td_topic)
        
        tbody.append(tr)
    
    # Write updated content back to file
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

if __name__ == "__main__":
    update_index_html()