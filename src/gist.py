import requests


def get_gist(auth_token: str, gist_id: str):
    # 需要获取的gist名字需要提前放在配置文件里面，建议写一个init过程
    # 这块的读取文档在 https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#get-a-gist

    # Define the URL for the GitHub API request
    url = f"https://api.github.com/gists/{gist_id}"

    # Set up the headers, including the authorization token and the API version
    headers = {
        "Authorization": f"token {auth_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Make the GET request to the GitHub API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        gist_data = response.json()
        print(gist_data)
    else:
        print(f"Failed to retrieve gist: {response.status_code}")
        print(response.text)


def put_gist():
    pass
