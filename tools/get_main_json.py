import requests
import json
import bs4
import sys
import os


main_url = f"https://www.angel.com/watch/"

temp_dir = './temp'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir, exist_ok=True)

response = requests.get(main_url)
soup = bs4.BeautifulSoup(response.content, 'html.parser')
main_data = json.loads(soup.find(id="__NEXT_DATA__").string)
# write out the json data to a file
with open(f'{temp_dir}/main_data.json', 'w') as f:
    json.dump(main_data, f, indent=2)