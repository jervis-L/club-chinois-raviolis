import requests
import json
# https://auth.viarezo.fr/oauth/authorize/?response_type=code&client_id=9f812cb77e1b92e5943ce4369d4c8ec187905105&redirect_uri=http://127.0.0.1:8000/&state=default&scope=default
class oauth_viarezo():
    def __init__(self):
        self.headers={'Content-Type': 'application/x-www-form-urlencoded',}
        self.client_id='9f812cb77e1b92e5943ce4369d4c8ec187905105'
        self.client_secret='9ecedfb573ded79960cc663be3fe4777575e7b8f'
        self.redirect_uri='http://cs-clubchinois-raviolis.herokuapp.com'
        # access_token本应存到session中,这里暂时用作内部变量
        # session的使用不是特别明晰,有时会出错
    def get_access_token(self, code):
        data = {'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
                'redirect_uri': self.redirect_uri}
        response = requests.post('https://auth.viarezo.fr/oauth/token/', headers=self.headers, data=data)
        json_response=json.loads(response.text)
        self.access_token=json_response["access_token"]
        self.refresh_token=json_response["refresh_token"]
        return self.access_token
    def get_user_info(self):
        headers2={'Authorization':'Bearer '+self.access_token,}
        rep2=requests.get('https://auth.viarezo.fr/api/user/show/me', headers=headers2)
        js_rep=json.loads(rep2.text)
        return js_rep

    def get_user_name(self):
        headers2={'Authorization':'Bearer '+self.access_token,}
        rep2=requests.get('https://auth.viarezo.fr/api/user/show/me', headers=headers2)
        js_rep=json.loads(rep2.text)
        first_name=js_rep["firstName"]
        last_name=js_rep["lastName"]
        name=last_name+' '+first_name
        return name
