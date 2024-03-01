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

def get_current_cname(zone_id, name):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=CNAME&name={name}"
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': api_key,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json()['result']:
        current_cname = response.json()['result'][0]['content']
        return current_cname
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

def check_and_update(domain, cname):
    current_cname = get_current_cname(zone_id, api_call_domain)
    if current_cname and current_cname == cname:
        print(f"{api_call_domain} 的CNAME记录已是 {cname}，无需更改。")
        return True
    if ping(domain):
        print(f"{domain} ping通了。")
        if current_cname != cname:
            print(f"当前CNAME记录为 {current_cname}，与目标 {cname} 不匹配，正在更新...")
            update_dns_record(zone_id, api_call_domain, cname)
        return True
    print(f"{domain} ping不通。")
    return False

def main_loop():
    while True:
        for attempt in range(3):
            if ping(api_call_domain):
                print(f"{api_call_domain}通畅")
                break
            else:
                print(f"{api_call_domain} ping不通，尝试次数：{attempt + 1}/3")
                time.sleep(5)
        else:  # 如果api_call_domain连续3次ping不通
            print(f"{api_call_domain}连续3次ping不通，开始检测cname1...")
            if not check_and_update(cname1, cname1):
                print(f"cname1 ({cname1}) 也不通，开始检测cname2...")
                check_and_update(cname2, cname2)
        time.sleep(10)  # 检查周期间隔

if __name__ == "__main__":
    main_loop()
