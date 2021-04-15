import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
  'client_id': 'AP',
  'client_secret': '4',
  'code': 'QeDNsifJ1VvC9087RbacfDMp3yWMZF',
  'redirect_uri': 'http://127.0.0.1:8000/',
  'grant_type': 'authorization_code'
}
# 似乎非常快就过期了？我也不知code为何刷新这么快,而且只能允许用一次
response = requests.post('http://127.0.0.1:8000/o/token/', headers=headers, data=data)
print(response.content)

# vGS5P36lPmcUwdgVjPzpjiNKa5UINe
# GLRw1DpNyT8LOaTaujbvqypxaCLLwm