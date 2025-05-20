import requests
import json
import bs4
import os
import logging
import urllib.parse

logger = logging.getLogger(__name__)

# Choose a logging level: logging.[INFO, DEBUG]
loglevel = logging.DEBUG
logging.basicConfig(level=loglevel)

"""Testing login and Whole Site Code!"""

username = "brian@reavey05.com"
password = "ClericalSupplierSillyRejoice"

ADDON_PATH = 'the path'
ICONS_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'icons')
FANART_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'fanart')
posters = os.path.join(ADDON_PATH, 'resources', 'images', 'posters')

picturepage = "https://zeroheight.com/41be3b805"
      #  This ^ is the page with cool project pictures
        #this is the picture I want: "https://zeroheight-user-uploads.s3.eu-west-1.amazonaws.com/user_attachments/275d9aacdc570843a165231a/Angel-Trades-Icon-App-1024x1024.png?response-content-disposition=inline&response-content-type=image%2Fpng&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA3AVNYHQK7P2O23UM%2F20241127%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Date=20241127T010645Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=0c71f5c0c63fc463ef49e4176ff8b8b771bc282d0a60555f189d9f2e9bc928c2"
mainpage='https://www.angel.com/watch'

session = requests.session()

auth_flow_start_url = 'https://www.angel.com/api/auth/login'
flow_page = session.get(auth_flow_start_url)
if flow_page.status_code == 200:
    logger.info("Successfully fetched the login page.")
    logger.debug(f"{flow_page.status_code=}")
else:
    logger.error(f"{flow_page.status_code=}")
    raise

cookies=flow_page.cookies
logger.debug(f"{cookies=}")

email_form_page_soup = bs4.BeautifulSoup(flow_page.content, "html.parser")

logger.debug(f"{email_form_page_soup=}")

state=None
for r_input in email_form_page_soup.find_all('input'):
    logger.debug(f"{r_input=}")
    if r_input.get('id') == 'state' and r_input.get('name') == 'state':
        state = r_input.get('value')

logger.debug(f"{state=}")

data = {
    'email': username,
    'state': state
}

encoded_data=urllib.parse.urlencode(data)
full_url = f"https://auth.angel.com/u/login/password?{encoded_data}"
logger.debug(f"{full_url=}")

response1 = session.get(full_url)

logger.debug(f"{response1.content=}")

soup2 = bs4.BeautifulSoup(response1.content, "html.parser")
state2 = None
csrf_token = None
for r_input in soup2.find_all('input'):
    logger.debug(f"{r_input=}")
    if r_input.get('id') == 'state' and r_input.get('name') == 'state':
        state2 = r_input.get('value')
    elif r_input.get('name') == '_csrf_token':
        csrf_token = r_input.get('value')

data2 = {
    'email': username,
    'password': password,
    'state': state2,
    '_csrf_token': csrf_token,
    'has_agreed': 'true'
}
logger.debug(json.dumps(data2, indent=2))

encoded2 = urllib.parse.urlencode({'state': state2})
post_url = f"https://auth.angel.com/u/login?{encoded2}"

logger.debug(f"{post_url=}")

response2 = session.post(post_url, data=data2)
if response2.status_code == 200:
    logger.info("Successfully logged into Angel Studios!")
logger.debug(f"{response2.cookies.get_dict()=}")
logger.debug(f"{response2.headers=}")

response = session.get(mainpage)
logger.debug(f"{response.cookies.get_dict()=}")

soup = bs4.BeautifulSoup(response.content, 'html.parser')

angeldata = json.loads(soup.find(id="__NEXT_DATA__").string)

with open('mainpage.json', 'w') as file:
    file.write(json.dumps(angeldata, indent=2))


for project_data in angeldata['props']['pageProps']['pageDataContext']['start-watching']:
    project_name = project_data['name']
    project_url = f"https://www.angel.com/watch/{project_data['track']['payload']['projectSlug']}"
    if project_url != 'https://www.angel.com/watch/tuttle-twins':
        continue
    print(f"{project_name} - {project_url}")
    response = session.get(project_url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    show_data = json.loads(soup.find(id="__NEXT_DATA__").string)


    if project_data['track']['payload']== None:
        continue
    elif project_data['track']['payload']['projectSlug'] == None:
        continue          
    elif show_data['props']['pageProps'] == None:
        continue
    elif show_data['props']['pageProps']['catalogTitle'] == None:
        continue

    seasons = []
    for raw_season in show_data['props']['pageProps']['projectData']['seasons']:
        season = {
                'name': raw_season['name'],
                'season_number': raw_season['episodes'][0]['seasonNumber'],
                'poster': f"{posters}/TT_{raw_season['name'].replace(' ', '')}_Poster.jpg",
                'description': show_data['props']['pageProps']['catalogTitle']['description']['long'],
                'episodes': None
            }
            

        print(f"    {season['name']} - {season['season_number']}")
        print(season)       
        episodes = []
        for episode in raw_season['episodes']:
        # xmbcplugin.log(episode['subtitle'])
            #xmbcplugin.log(episode['source']['url'])
            if episode['source']== None:
                continue            
            elif episode['source']['url'] == None:
                continue       
            # find out how to use 'continue' to skip episodes
            episode = {
                'episode_name': episode['name'],
                'title': episode['subtitle'],
                # The full name of the episode:
                'name': f"{episode['name']}: {episode['subtitle']}",
                'episode_number': episode['episodeNumber'],
                'poster': f"https://images.angelstudios.com/image/upload/f_auto/q_auto/{episode['posterLandscapeCloudinaryPath']}.jpg",
                'url': episode['source']['url'],
                'description': episode['description'],
            } 
            print(f"        {episode['episode_number']} - {episode['episode_name']}")

            episodes.append(episode)
            season['episodes'] = episodes
        seasons.append(season)

