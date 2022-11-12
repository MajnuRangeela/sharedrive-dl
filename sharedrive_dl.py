import requests
from urllib.parse import urlparse

link = ""  #file url

'''
NOTE:
DO NOT use the logout button on website. Instead, clear the site cookies manually to log out.
If you use logout from website, cookies will become invalid. This cookie will be expired automatically after
a month, so you will need to regrenerate cookie every month.
'''
PHPCKS = ""

#=====================================================================================================================================================================

def shareDrive(url,directLogin=True):

    scrapper = requests.Session()

    #retrieving session PHPSESSID
    cook = scrapper.get(url)
    cookies = cook.cookies.get_dict()
    PHPSESSID = cookies['PHPSESSID']

    headers = {
        'authority' : urlparse(url).netloc,
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin' : f'https://{urlparse(url).netloc}/',
        'referer' : url,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
        'X-Requested-With	' : 'XMLHttpRequest'
    }

    if directLogin==False:
        cookies = {
            'PHPSESSID' : PHPSESSID,
            'PHPCKS' : PHPCKS
        }

        data = {
            'id' : url.rsplit('/',1)[1],
            'key' : 'original'
        }
    else:
        cookies = {
            'PHPSESSID' : PHPSESSID
        }

        data = {
            'id' : url.rsplit('/',1)[1],
            'key' : 'direct'
        }

    
    resp = scrapper.post(f'https://{urlparse(url).netloc}/post', headers=headers, data=data, cookies=cookies)

    if directLogin==False:
        driveUrl = resp['redirect']
        return driveUrl
    else:
        try:
            toJson = resp.json()
            driveUrl = toJson['redirect']
            return driveUrl
        except:
            if len(PHPCKS)>0:
                shareDrive(url,directLogin=False)
            else:
                raise Exception('Direct Login is not there and you have not provided PHPCKS cookie value!!')

                
gDriveURL = shareDrive(link)
print(gDriveURL)

#==============================================================================================================================================================

''' Sample Output of respone json file

{'error': '0', 'message': 'Success', 'redirect': 'https://drive.google.com/uc?id=1l_CLYBX2tdhtrhrt1eQhiaJjMvyw7Yb'}

*NOTE: This Script by default returns Google Drive URL, json response sample is provided only for knowledge purpose.
'''
