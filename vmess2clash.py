import base64
import json
import yaml
import os
from dotenv import load_dotenv
load_dotenv()

# 原始vmess链接
vmess_link = os.getenv("VMESS")

# 去除前缀并解码Base64
vmess_encoded = vmess_link.replace("vmess://", "")
vmess_decoded = base64.b64decode(vmess_encoded).decode('utf-8')

# 解析为JSON
vmess_config = json.loads(vmess_decoded)

# Clash配置格式
clash_config = {
    "proxies": [
        {
            "name": vmess_config["ps"],
            "type": "vmess",
            "server": vmess_config["add"],
            "port": vmess_config["port"],
            "uuid": vmess_config["id"],
            "alterId": int(vmess_config["aid"]),
            "cipher": "auto",
            "udp": True,
            "tls": True if vmess_config["tls"] == "tls" else False,
            "skip-cert-verify": True,
            "network": vmess_config["net"],
            "ws-opts": {
                "path": vmess_config["path"]
            }
        }
    ]
}

# 将配置转换为YAML格式
clash_config_yaml = yaml.dump(clash_config, allow_unicode=True, sort_keys=False)

# 将YAML内容写入文件
with open("azure.yaml", "w", encoding='utf-8') as file:
    file.write(clash_config_yaml)

print("Finished!")
