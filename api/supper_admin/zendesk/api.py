import requests

url = "https://usdctechnology.zendesk.com/api/v2/oauth/tokens.json"

payload = "{\"token\": {\"client_id\": 900000037863, \"scopes\": [\"read\", \"write\"]}}"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic Y3Vvbmdsc0B1c2RjLnZuL3Rva2VuOksyY2dtZU80dFlsTVpZa0ZQcTJLMmF5WXpZVXM5aGJyTmYyMDk5TjM=',
    'Cookie': '__cfduid=d20d1a835cabe8587f18485732ff8210e1600165733; __cfduid=d684e3d5bf9003e425777ab289d48a02e1600173561; __cfruid=1ebfcef2b234cb591c0476580ca81f558e08237a-1600659615'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text.encode('utf8'))
