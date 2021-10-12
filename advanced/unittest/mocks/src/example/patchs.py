import requests

def call_api(user, password):

    r = requests.get(f'https://api.github.com/{user}', auth=(user, password))
    print(r)
    if r.status_code == 200:
        r.json()
        return r
    else:
        print("Invalid call")
        return None

def read_file(path):

    with open(path, "r") as f:
        info = f.read()

    return info

