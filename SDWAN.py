import requests
import sys
import base64

def getStatsDb(baseurl, user, password):
    url = f"{baseurl}/management/elasticsearch/index/size"
    payload={}
    basicauth=f'{user}:{password}'
    b64auth = base64.b64encode(basicauth.encode('ascii')).decode('ascii')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {b64auth}'
    }

    response = requests.get(url, headers=headers, verify=False).text
    return response

if __name__ == '__main__':
    print(getStatsDb(sys.argv[1],sys.argv[2]))