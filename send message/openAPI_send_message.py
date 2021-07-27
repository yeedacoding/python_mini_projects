import json
import requests
import datetime
import os


url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": "(REST_API 앱 키)",
    "redirect_uri": "https://localhost.com",
    "code": "(발급받은 인증 코드)"
}

response = requests.post(url, data=data)

tokens = response.json()


# 카카오 토큰을 저장할 파일명
KAKAO_TOKEN_FILENAME = "res/kakao_message/kakao_token.json"

# 토큰을 저장하는 함수


def save_tokens(filename, tokens):
    with open(filename, "w") as fp:
        json.dump(tokens, fp)

# 토큰을 읽어오는 함수


def load_tokens(filename):
    with open(filename) as fp:
        tokens = json.load(fp)

    return tokens


# refresh_token으로 access_token을 갱신하는 함수

def update_tokens(app_key, filename):
    tokens = load_tokens(filename)

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": app_key,
        "refresh_token": tokens['refresh_token']
    }
    response = requests.post(url, data=data)

    # 요청에 실패했다면?
    if response.status_code != 200:
        print("error! because ", response.json())
        tokens = None
    else:  # 성공했다면,
        print(response.json())
        # 기존 파일 백업
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = filename+"."+now
        os.rename(filename, backup_filename)
        # 갱신된 토큰 저장
        tokens['access_token'] = response.json()['access_token']
        save_tokens(filename, tokens)

    return tokens


# 토큰 저장
save_tokens(KAKAO_TOKEN_FILENAME, tokens)

# access_token이 유효하지 않은 경우?  --> update_tokens함수를 호출하여 재발급
# KAKAO_APP_KEY = "(REST_API APP KEY)"
# tokens = update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)
# save_tokens(KAKAO_TOKEN_FILENAME, tokens)

##############################################################################################
##############################################################################################
# 텍스트 템플릿 메세지 보내기

# 저장된 토큰 정보를 읽어 옴
tokens = load_tokens(KAKAO_TOKEN_FILENAME)

# 텍스트 메시지 url
url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# request parameter 설정
headers = {
    "Authorization": "Bearer " + tokens['access_token']
}

data = {
    "template_object": json.dumps({"object_type": "text", "text": "Hello, world!", "link": {"web_url": "www.naver.com"}})
}

# 나에게 카카오톡 메시지 보내기 요청(text)
response = requests.post(url, headers=headers, data=data)
print(response.status_code)

# 요청에 실패했다면,
if response.status_code != 200:
    print("error! because ", response.json())
else:  # 성공했다면
    print('메시지를 성공적으로 보냈습니다.')

##############################################################################################
##############################################################################################
# 리스트 템플릿 메세지 보내기

# 저장된 토큰 정보를 읽어 옴
tokens = load_tokens(KAKAO_TOKEN_FILENAME)

# 텍스트 메시지 url
url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# request parameter 설정
headers = {
    "Authorization": "Bearer " + tokens['access_token']
}

template = {
    "object_type": "list",
    "header_title": "초밥 사진",
    "header_link": {
        "web_url": "www.naver.com",
        "mobile_web_url": "www.naver.com"
    },
    "contents": [
        {
            "title": "1. 광어초밥",
            "description": "광어는 맛있다",
            "image_url": "https://search1.kakaocdn.net/argon/0x200_85_hr/8x5qcdbcQwi",
            "image_width": 50, "image_height": 50,
            "link": {
                "web_url": "www.naver.com",
                "mobile_web_url": "www.naver.com"
            }
        },
        {
            "title": "2. 참치초밥",
            "description": "참치는 맛있다",
            "image_url": "https://search2.kakaocdn.net/argon/0x200_85_hr/IjIToH1S7J1",
            "image_width": 50, "image_height": 50,
            "link": {
                "web_url": "www.naver.com",
                "mobile_web_url": "www.naver.com"
            }
        }
    ],
    "buttons": [
        {
            "title": "웹으로 이동",
            "link": {
                "web_url": "www.naver.com",
                "mobile_web_url": "www.naver.com"
            }
        }
    ]
}

data = {
    "template_object": json.dumps(template)
}
# 나에게 카카오톡 메시지 보내기 요청(text)
response = requests.post(url, data=data, headers=headers)
print(response.status_code)


# 요청에 실패했다면,
if response.status_code != 200:
    print("error! because ", response.json())
else:  # 성공했다면
    print('메시지를 성공적으로 보냈습니다.')
