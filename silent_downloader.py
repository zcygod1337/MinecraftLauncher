import argparse
import requests
import os
from urllib.parse import urlparse
# 禁用SSL验证警告
requests.packages.urllib3.disable_warnings()

def silent_download(url):
    try:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) or "downloaded_file"
        save_path = os.path.join(os.getcwd(), filename)
        
        with requests.get(url, stream=True, timeout=10, verify=False) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"下载完成: {filename}")
        
    except Exception as e:
        print(f"下载失败: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', required=True)
    args = parser.parse_args()
    silent_download(args.url)
