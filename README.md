# auto-cname-api-for-cloudflare


利用cloudflare自动切换cname 记录
"cloudflare_email": 你的Cloudflare账户邮箱。
"cloudflare_api_key": 你的Cloudflare API密钥。
"cloudflare_zone_id": 你想要修改DNS记录的域名所在的Zone ID。


确保替换config.json中的配置信息为你自己的实际信息。
脚本使用requests库来调用Cloudflare API，因此请确保已安装该库（使用命令pip install requests安装）。
本脚本使用了ping命令进行连通性检测，这在某些环境中可能需要适当的权限。
脚本中的time.sleep(10)用于在每次检测周期后等待10秒，你可以根据需要调整这个时间间隔。
这个脚本实现了一个基本的循环逻辑，定期检查API调用域名的连通性，并根据配置的备选CNAME记录更新DNS设置。