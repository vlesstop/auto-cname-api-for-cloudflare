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




安装pip
对于Python 3.6
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