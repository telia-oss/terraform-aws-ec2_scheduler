import boto3
from datetime import datetime, timedelta
import os
import json
import pytz

REGIONS = json.loads(os.environ.get('REGIONS', '["eu-north-1", "eu-west-1", "eu-central-1", "us-west-1"]'))
#LOCAL_TIMEZONE = pytz.timezone('Europe/Stockholm')
LOCAL_TIMEZONE = pytz.timezone(os.environ.get('TIMEZONE', 'Europe/Stockholm'))
TIME_WINDOW_MINUTES = 10

def is_within_time_window(tag_time_str, current_time):
    try:
        tag_time = datetime.strptime(tag_time_str, '%H:%M').time()
        tag_dt = datetime.combine(datetime.today(), tag_time)
        current_dt = datetime.combine(datetime.today(), current_time)
        delta = abs((tag_dt - current_dt).total_seconds()) / 60
        return delta <= TIME_WINDOW_MINUTES
    except ValueError:
        return False

def lambda_handler(event, context):
    now_local = datetime.now(LOCAL_TIMEZONE)
    now_time = now_local.time()
    print(f"Current local time ({LOCAL_TIMEZONE}): {now_local.strftime('%H:%M')}")

    for region in REGIONS:
        print(f"\nChecking region: {region}")
        ec2 = boto3.resource('ec2', region_name=region)

        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
            ]
        )

        for instance in instances:
            instance.load()
            tags = {tag['Key'].lower(): tag['Value'] for tag in (instance.tags or [])}
            stop_at = tags.get('stop_at')
            start_at = tags.get('start_at')

            print(f"\nInstance ID: {instance.id}")
            print(f"State: {instance.state['Name']}")
            print(f"Tags: {tags}")            

            if stop_at and is_within_time_window(stop_at, now_time) and instance.state['Name'] == 'running':
                print(f">>> [Action] Stopping instance {instance.id} in {region}")
                instance.stop()

            elif start_at and is_within_time_window(start_at, now_time) and instance.state['Name'] == 'stopped':
                print(f">>> [Action] Starting instance {instance.id} in {region}")
                instance.start()

            else:
                print(f">>> No action taken for instance {instance.id}")
