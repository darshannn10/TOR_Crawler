import requests
session = requests.session()
session.proxies = {'http':  'socks5h://localhost:9150',
                   'https': 'socks5h://localhost:9150'}
print(session.get('http://httpbin.org/ip').text) # prints {"origin": "67.205.146.164" }

print(requests.get('http://httpbin.org/ip').text) # prints {"origin": "5.102.254.76" }

print(session.get('http://nzxj65x32vh2fkhk.onion/all').text) # Prints the contents of the page
#http://ednf5xiofeunsycu.onion/wiki-onion-urls.html
