# API 호출을 위해 requests 모듈을 사용
import requests

# API 에서 공통적으로 사용하는 텍스트를 선언
apiDefault = {
    'region': 'https://kr.api.riotgames.com',  # 한국서버를 대상으로 호출
    'key': 'RGAPI-c47e074a-2eaf-4301-acd8-0e96016f12a5',  # API KEY 
    'summonerName': 'Hide on Bush',  # 닉네임
}

# api 호출시 사용되는 url
url = f"{apiDefault['region']}/lol/summoner/v4/summoners/by-name/{apiDefault['summonerName']}?api_key={apiDefault['key']}"

# get method 를 통해 api 호출
req = requests.get(url)

req_dict = eval(req.text)

print(req_dict['id'])

#print(req.text)['id'])