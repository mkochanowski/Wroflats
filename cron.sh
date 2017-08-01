#! /bin/bash    
cd /home/marek/wroflats
source venv/bin/activate

python3 scrap_gumtree.py
python3 scrap_gumtree_item.py
python3 calculate_rating.py