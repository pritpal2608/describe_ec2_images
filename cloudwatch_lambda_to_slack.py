# Script used with a Lambda function to take payload from Cloudwatch 
# Perform formating, Then send on to Slack Webhook.
# Replaced by sending Cloudwatch event to Pagerduty.

!/usr/bin/python3.6
import urllib3
import json
http = urllib3.PoolManager()
def lambda_handler(event, context):
    url = "https://hooks.slack.com/services/[ Enter Webhook ]"
    rawmessage = json.loads(json.dumps(event['Records'][0]['Sns']['Message']).replace("\\","")[1:-1])
    # Above fetch the Message from Alarm, strips \ and front and trailing "
    msg = {
        "channel": "pritpal-test",
        "username": "WEBHOOK_USERNAME",
        "text":  "*Alarm-Name*             "+ json.dumps(rawmessage['AlarmName']) +
        "\n"+ ">*Reason for Alarm is*        "+ json.dumps(rawmessage['NewStateReason'])+
        "\n"+ ">*AlarmARN*                       "+  json.dumps(rawmessage['AlarmArn']) +
        "\n"+ ">*TargetGroup Affected*           "+  json.dumps(rawmessage['Trigger']['Dimensions'][0]['value'])+
        "\n"+ ">*Loadbalancer Affected*          "+  json.dumps(rawmessage['Trigger']['Dimensions'][1]['value']),
        #"text": json.dumps(event),  # Used to expose payload in raw format slack channel
        "icon_emoji": ":aws-logo:"
    }
    
    #encoded_msg = json.dumps(msg).encode('utf-8')
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)
    print(
        {
        "message": event['Records'][0]['Sns'], 
        "status_code": resp.status, 
        "response": resp.data
    })