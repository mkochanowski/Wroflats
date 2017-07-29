#! /bin/bash    
cd /usr/local/bin/scraping/wroflats
source venv/bin/activate

python3 scrap_gumtree.py
python3 scrap_gumtree_item.py
