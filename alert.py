import json
import requests
from elasticsearch import Elasticsearch
import urllib3

#this will disable warning for https
urllib3.disable_warnings()

#this line define your elaticsearch host

host = Elasticsearch([{'host': <your-elastic-host>, 'port': <your-elastic-port>}], http_auth=(<your-elastic-user>, <your-elastic-password>))

#this part of code is so important. you define your query to get detailes from elasticsearch. the below query will grep thoes messages that contain failed word in the last 30m. you can use whatever supported elastic query you want.
response = host.search(
    index=<your-auth-log-index>,
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

#this file contain slack webhook.
credentials = '/path/to/credentials.json'
 
def get_credentials(credentials):
    '''
    Read credentials from JSON file.
    '''
    with open(credentials, 'r') as f:
        creds = json.load(f)
    return creds['slack_webhook']

for hit in response['hits']['hits']:
    message = hit['_source']['message']
    print(message)
    data = {'text':message}
    url = get_credentials(credentials)
    requests.post(url,json=data, verify=False)
