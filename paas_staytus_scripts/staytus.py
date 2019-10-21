###
#
#
import requests

class StaytusClient:
  def __init__(self, url, token, secret):
    self.url = url
    self.token = token
    self.secret = secret

  def get_open_issues(self,service_name):
    headers = { 'X-Auth-Token': '%s' % self.token, 'X-Auth-Secret': '%s' % self.secret}
 
    staytus_url = self.url + "/api/v1/issues/all"
 
    response = requests.get(staytus_url, headers=headers)
 
    issues = response.json()['data']
 
    filtered_issues = [issue for issue in issues if(issue['state'] == 'investigating' and service_name in (issue['title']))]
 
    return filtered_issues 

  def create_issue(self, service_name, service_permalink, issue_status_permalink, error_message):
     # call staytus API to change the status
    headers = { 'X-Auth-Token': '%s' % self.token, 'X-Auth-Secret': '%s' % self.secret, 'Content-Type': 'application/json' }
 
    staytus_url = self.url + "/api/v1/issues/create"
 
    payload = {
      "title": service_name + " issue",
      "initial_update": error_message,
      "state": "investigating",
      "services": [ service_permalink ],
      "status": issue_status_permalink,
      "notify": True
    }
 
    response = requests.post(staytus_url, json=payload, headers=headers)

  def update_issue(self, issue_id, service_status):
    headers = { 'X-Auth-Token': '%s' % self.token, 'X-Auth-Secret': '%s' % self.secret, 'Content-Type': 'application/json' }
 
    staytus_url = self.url + "/api/v1/issues/update"
 
    payload = {
      "id": issue_id,
      "text": "The problem has been fixed",
      "state": "resolved",
      "status": service_status,
      "notify": True
    }
 
    response = requests.post(staytus_url, json=payload, headers=headers)
  
