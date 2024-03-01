# -*- coding: utf-8 -*-

import json
import subprocess
import requests
import time

# 加载配置文件
with open('config.json', 'r') as file:
    config = json.load(file)

cname1 = config['cname1']
cname2 = config['cname2']
api_call_domain = config['api_call']
email = config['cloudflare_email']
api_key = config['cloudflare_api_key']
zone_id = config['cloudflare_zone_id']

def ping(domain):
    try:
        subprocess.check_output(['ping', '-c', '1', '-W', '5', domain], stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

def perform_ping_checks(domain):
    """Perform 3 ping checks for a given domain."""
    for _ in range(3):
        if ping(domain):
            return True
        time.sleep(5)
    return False

def get_current_cname(zone_id, name):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=CNAME&name={name}"
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': api_key,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json()['result']:
        return response.json()['result'][0]['content']
    else:
        print(f"获取当前CNAME记录失败: {response.text}")
        return None

def update_dns_record(zone_id, name, content):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': api_key,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers, params={'name': name, 'type': 'CNAME'})
    if response.status_code == 200 and response.json()['result']:
        record_id = response.json()['result'][0]['id']
        data = {
            'type': 'CNAME',
            'name': name,
            'content': content,
            'ttl': 1,
        }
        update_response = requests.put(f"{url}/{record_id}", headers=headers, json=data)
        if update_response.status_code == 200:
            print(f"DNS记录更新成功: {name} -> {content}")
        else:
            print(f"DNS记录更新失败: {update_response.text}")
    else:
        print(f"未找到DNS记录: {name}")

def main_loop():
    while True:
        # Check api_call_domain with 3 attempts
        if not perform_ping_checks(api_call_domain):
            current_cname = get_current_cname(zone_id, api_call_domain)
            # Check cname1 with 3 attempts
            if perform_ping_checks(cname1):
                if current_cname != cname1:
                    update_dns_record(zone_id, api_call_domain, cname1)
            else:
                # Check cname2 with 3 attempts if cname1 fails
                if perform_ping_checks(cname2):
                    if current_cname != cname2:
                        update_dns_record(zone_id, api_call_domain, cname2)
        else:
            print(f"{api_call_domain} 通畅，可以访问.")
        time.sleep(10)

if __name__ == "__main__":
    main_loop()
