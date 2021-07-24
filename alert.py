import json
import requests
from elasticsearch import Elasticsearch
import urllib3

urllib3.disable_warnings()

host = Elasticsearch([{'host': '<elasticsearch host>', 'port': '<elasticsearch port>'}], http_auth=('<elasticsearch username>', '<elasticsearch password>'))

proxies = { #comment this part if you don't want to use socks5 proxy
        'http': 'socks5h://',
        'https': 'socks5h://'
}

def failed_login():
  response = host.search(
    index="auth-log",
    body={
   "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "Failed password"
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

  for hit in response['hits']['hits']:
    message = hit['_source']['message']
    print(message)
    data = {'text':message}
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
    requests.get(send_text, proxies=proxies) #comment proxies if you don't want use socks5 proxy


def main():
  failed_login()

if __name__ == "__main__":
  main()
