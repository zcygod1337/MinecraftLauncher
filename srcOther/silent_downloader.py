import argparse
import requests
import os
import sys
import time
from urllib.parse import urlparse

# 禁用SSL验证警告
requests.packages.urllib3.disable_warnings()

def print_progress(progress, total=None, bar_length=50):
    """打印进度条，支持未知总大小的情况"""
    # 格式化文件大小显示
    progress_size = format_file_size(progress)
    
    if total is None or total == 0:
        # 未知总大小，只显示已下载大小
        sys.stdout.write(f'\r已下载: {progress_size}')
    else:
        # 已知总大小，显示完整进度条
        percent = float(progress) / total
        filled_length = int(bar_length * progress // total)
        bar = '#' * filled_length + '-' * (bar_length - filled_length)
        total_size = format_file_size(total)
        sys.stdout.write(f'\r[{bar}] {percent:.1%} ({progress_size}/{total_size})')
    
    sys.stdout.flush()

def format_file_size(size):
    """格式化文件大小显示（B, KB, MB, GB）"""
    units = ['B', 'KB', 'MB', 'GB']
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
        
    return f"{size:.2f} {units[unit_index]}"

def silent_download(url):
    try:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) or "downloaded_file"
        save_path = os.path.join(os.getcwd(), filename)
        
        # 尝试获取文件大小（处理可能的失败）
        file_size = 0
        try:
            with requests.head(url, timeout=10, verify=False, allow_redirects=True) as head_r:
                head_r.raise_for_status()
                file_size = int(head_r.headers.get('content-length', 0))
        except:
            print("无法获取文件大小，将显示已下载大小")
        
        # 下载文件并显示进度条
        with requests.get(url, stream=True, timeout=10, verify=False) as r:
            r.raise_for_status()
            
            downloaded_size = 0
            last_update_time = 0
            update_interval = 0.1  # 限制更新频率，避免刷新太快
            
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # 控制更新频率
                        current_time = time.time()
                        if current_time - last_update_time > update_interval or (file_size and downloaded_size >= file_size):
                            print_progress(downloaded_size, file_size)
                            last_update_time = current_time
        
        # 确保最后输出一个换行
        print()
        print(f"下载完成: {filename}")
        
    except Exception as e:
        print(f"\n下载失败: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', required=True)
    args = parser.parse_args()
    silent_download(args.url)
    
