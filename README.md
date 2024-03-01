# auto-cname-api-for-cloudflare
cname1 为 备用cname 记录
cname2 为 备用cname 记录
api_call为要修改的域名记录
cloudflare_zone_id 为：区域 ID
区域ID 查找方法：打开域名， 点击概述， 拉到最下方，在右侧  英文为：zone_id 

利用cloudflare自动切换cname 记录
"cloudflare_email": 你的Cloudflare账户邮箱。
"cloudflare_api_key": 你的Cloudflare API密钥。
"cloudflare_zone_id": 你想要修改DNS记录的域名所在的Zone ID。
# 使用方法
建议放到root目录下，新建文件夹 autocname
cd /root/autocname 
python3 auto.py   //前台运行
nohup python3 auto.py &

确保替换config.json中的配置信息为你自己的实际信息。
脚本使用requests库来调用Cloudflare API，因此请确保已安装该库（使用命令pip install requests安装）。
本脚本使用了ping命令进行连通性检测，这在某些环境中可能需要适当的权限。
这个脚本实现了一个基本的循环逻辑，定期检查API调用域名的连通性，并根据配置的备选CNAME记录更新DNS设置。

## 关于必须安装的依赖
安装pip
# Python 3.6建议使用， 不推荐使用Python 3.6以下版本
大多数现代Linux发行版和macOS系统已经预安装了Python 3和pip。如果你的系统中没有pip3，你可能需要手动安装它。
在Linux上：
如果你使用的是Debian/Ubuntu及其衍生版，可以使用以下命令安装：

bash
Copy code
sudo apt update
sudo apt install python3-pip
对于Fedora：

bash
Copy code
sudo dnf install python3-pip
sudo yum install rh-python36

对于CentOS/RHEL，CentOS 7及以下版本可能需要先启用EPEL仓库：

bash
Copy code
sudo yum install epel-release
sudo yum install python3-pip
在macOS上：

通常，安装Python 3（从Python.org或使用Homebrew）时会自带pip3。如果需要安装或更新pip，可以使用以下命令：

bash
Copy code
sudo python3 -m ensurepip --upgrade
