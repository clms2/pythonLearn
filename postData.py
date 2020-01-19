import urllib.request
import urllib.parse

data = {
    "info": [
        {
            "order_id": 350229,
            "reasons": ["频繁发表负面言论或诋毁稻草人品牌，无法融入团队，与稻草人理念不符"]
        }
    ]
}

data = urllib.parse.urlencode(data)
data = bytes(data, 'utf-8')
response = urllib.request.urlopen("https://postUrl", data)
print(response.read().decode('unicode-escape'))
