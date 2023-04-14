import json, requests, os, time
from dotenv import load_dotenv

load_dotenv()

headers= {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json',
    'x-wink-api-key': os.getenv('API_KEY'),
    'Host': 'api.winktesting.com',
    'Authorization': os.getenv('TOKEN'),
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Wink/1 CFNetwork/1408.0.1 Darwin/22.5.0',
    'Connection': 'keep-alive',
    'Content-Length': '0'
}

alternative_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': os.getenv('COOKIE'), 
    'Host': 'app-images-alt.winktesting.com',
    'User-Agent': 'Wink/1 CFNetwork/1408.0.1 Darwin/22.5.0',
}

def retrieveData():
    t1 = time.time()
    r = requests.get('https://api.winktesting.com/api/v1/chats/friends?page=1&pageSize=800&type=all', headers=headers)
    
    if r.status_code == 200:
        t2 = time.time()
        total_time = round(t2 - t1, 3)
        print(f'Elapsed time: {total_time} seconds')
        data = r.json()
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print('Data retrieved successfully!')
    else:
        print('Failed to retrieve data!')

def downloadImages():
    with open('data.json', 'r') as f:
        data = json.load(f)
        for user in data:
            images = user['user_images']
            for image in images:
                url = image['image_url']
                r = requests.get(url, headers=alternative_headers)
                if r.status_code == 200:
                    if not os.path.exists('images'):
                        os.mkdir('images')
                    with open(f'images/{user["id"]}.jpg', 'wb') as f:
                        f.write(r.content)
                        print(f'Downloaded image for {user["id"]}')
                else:
                    print(f'Failed to download image for {user["id"]} Status code: {r.status_code}')

def parseIDs():
    with open('data.json', 'r') as f:
        data = json.load(f)
        ids = []
        for user in data:
            ids.append(user['id'])
    # print(ids)
    return ids

def unfriend(user_id):
    if type(user_id) == list:
        for user in user_id:
            unfriend(user)
    else:
        r = requests.post(f'https://api.winktesting.com/api/v1/users/unfriend/{user_id}', headers=headers)
        if r.status_code == 200:
            print(f'Unfriended {user_id}')
        else:
            print(f'Failed to unfriend {user_id}')
        
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

ascii = """

    mihai dragomir (8xu) april 2023. twitter: @wlmihai

"""

lines = ascii.split('\n')
def print_ascii(scroll_effect=True):
    for line in lines:
        print(line)
        if scroll_effect:
            time.sleep(0.01)

if __name__ == '__main__':
    try:
        while True:
            clear_screen()
            print_ascii()

            print("1. Retrieve data\n2. Parse IDs\n3. Unfriend\n4. Download images\n\n0. Exit")

            match input('\nEnter your choice: '):
                case '1':
                    retrieveData()
                    break
                case '2':
                    print(f'You have {len(parseIDs())} friends!')
                    break
                case '3':
                    unfriend(parseIDs())
                    break
                case '4':
                    downloadImages()
                    break
                case '0':
                    exit()
                case _:
                    print('Invalid choice!')
    except KeyboardInterrupt:
        print('Exiting...')
        exit()