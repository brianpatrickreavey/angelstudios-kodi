import requests
import json
import bs4
import sys


if len(sys.argv) < 2:
    project_slug = 'tuttle-twins'
else:
    project_slug = sys.argv[1]

project_url = f"https://www.angel.com/watch/{project_slug}"

response = requests.get(project_url)
soup = bs4.BeautifulSoup(response.content, 'html.parser')
show_data = json.loads(soup.find(id="__NEXT_DATA__").string)
# write out the json data to a file
with open(f'project_{project_slug}.json', 'w') as f:
    json.dump(show_data, f, indent=2)