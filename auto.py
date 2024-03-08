import json
import subprocess
import requests
import time
import logging

logging.basicConfig(filename='dns_checker.log', level=logging.DEBUG)

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
    """Perform 3 ping checks for a given domain and return True if any succeed."""
    for attempt in range(3):
        if ping(domain):
            logging.info(f"{domain} 通畅，可以访问.")
            return True
        else:
            logging.warning(f"{domain} ping不通，尝试次数：{attempt + 1}/3")
            time.sleep(5)
    logging.error(f"{domain} 连续3次ping不通。")
    return False

def get_current_cname(zone_id, name):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=CNAME&name={name}"
        headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': api_key,
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses
        if response.status_code == 200 and response.json()['result']:
            return response.json()['result'][0]['content']
        else:
            logging.error(f"获取当前CNAME记录失败: {response.text}")
            return None
    except Exception as e:
        logging.error(f"获取当前CNAME记录失败: {e}")
        return None

def update_dns_record(zone_id, name, content):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': api_key,
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers, params={'name': name, 'type': 'CNAME'})
        response.raise_for_status() # Raise an HTTPError for bad responses
        if response.status_code == 200 and response.json()['result']:
            record_id = response.json()['result'][0]['id']
            data = {
                'type': 'CNAME',
                'name': name,
                'content': content,
                'ttl': 1,
            }
            update_response = requests.put(f"{url}/{record_id}", headers=headers, json=data)
            update_response.raise_for_status() # Raise an HTTPError for bad responses
            if update_response.status_code == 200:
                logging.info(f"DNS记录更新成功: {name} -> {content}")
            else:
                logging.error(f"DNS记录更新失败: {update_response.text}")
        else:
            logging.error(f"未找到DNS记录: {name}")
    except Exception as e:
        logging.error(f"更新DNS记录失败: {e}")

def main_loop():
    while True:
        try:
            if not perform_ping_checks(api_call_domain):
                current_cname = get_current_cname(zone_id, api_call_domain)
                if current_cname != cname1 and perform_ping_checks(cname1):
                    update_dns_record(zone_id, api_call_domain, cname1)
                elif current_cname != cname2 and perform_ping_checks(cname2):
                    update_dns_record(zone_id, api_call_domain, cname2)
                else:
                    logging.error("所有备选域名检测均不通畅，无法更新DNS记录。")
            time.sleep(10)  # 检查周期间隔
        except Exception as e:
            logging.error(f"发生异常: {e}")

if __name__ == "__main__":
    main_loop()
