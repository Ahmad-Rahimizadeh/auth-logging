import json
import requests
from elasticsearch import Elasticsearch
import urllib3

urllib3.disable_warnings()

#define your elasticsearch 
host = Elasticsearch([{'host': '', 'port': ''}], http_auth=('<elastic user>', '<elastic password>'))

#searching for faild in message field inside auth-index in last 30m.
response = host.search(
    index="auth-log",
    body={
   "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "failed"
          }
        },{
          "range": {
            "@timestamp": {
               "gte": "now-30m"

            }
          }
        }
      ]
    }
  }
}
)

#define proxy if you are in somewhere that telegram not working without proxy
proxies = {
        'http': 'socks5h://',
        'https': 'socks5h://'
}


for hit in response['hits']['hits']:
    message = hit['_source']['message']
    print(message)
    data = {'text':message}
    bot_token = ''
    bot_chatID = '' #your telegram channel id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
    requests.get(send_text, proxies=proxies)
