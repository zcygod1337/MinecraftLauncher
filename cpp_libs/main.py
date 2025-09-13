import argparse
import json
import os
import requests
import hashlib
import sys
import platform
import subprocess
from shutil import rmtree

# 全局进度跟踪变量
total_download_size = 0
downloaded_size = 0

def get_os():
    """获取当前操作系统"""
    os_name = platform.system().lower()
    if os_name == "windows":
        return "windows"
    elif os_name == "linux":
        return "linux"
    elif os_name == "darwin":
        return "osx"
    return None

def print_progress(width=50):
    """单行显示的总进度条"""
    global downloaded_size, total_download_size
    
    if total_download_size == 0:
        return
        
    percent = (downloaded_size / total_download_size) * 100
    filled = int(width * downloaded_size // total_download_size)
    bar = '█' * filled + '-' * (width - filled)
    progress_size = format_size(downloaded_size)
    total_size = format_size(total_download_size)
    sys.stdout.write(f'\r|{bar}| {percent:.1f}% {progress_size}/{total_size}')
    sys.stdout.flush()
    if downloaded_size >= total_download_size:
        print()

def format_size(bytes, suffix='B'):
    """格式化文件大小显示"""
    factor = 1024
    for unit in ['', 'K', 'M', 'G']:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
    return f"{bytes:.2f}T{suffix}"

def get_version_manifest():
    """获取Minecraft版本清单"""
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取版本清单失败: {e}")
        return None

def find_version_info(manifest, version):
    """查找指定版本的信息"""
    if not manifest:
        return None
    
    # 支持最新版本
    if version.lower() == "latest":
        latest_release = manifest["latest"]["release"]
        for v in manifest["versions"]:
            if v["id"] == latest_release:
                return v
    
    # 查找指定版本
    for v in manifest["versions"]:
        if v["id"] == version:
            return v
    
    print(f"未找到版本: {version}")
    return None

def get_version_details(version_info):
    """获取版本详细信息"""
    try:
        response = requests.get(version_info["url"])
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取版本详情失败: {e}")
        return None

def download_file(url, save_path):
    """下载文件并更新总进度"""
    global downloaded_size
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            file_size = int(r.headers.get('content-length', 0))
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 检查文件是否已存在且完整
            if os.path.exists(save_path) and os.path.getsize(save_path) == file_size:
                downloaded_size += file_size
                print_progress()
                return True
            
            with open(save_path, 'wb') as f:
                downloaded_file = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_file += len(chunk)
                        downloaded_size += len(chunk)
                        print_progress()
        
        return True
    except Exception as e:
        print(f"\n下载失败: {e}")
        if os.path.exists(save_path):
            os.remove(save_path)
        return False

def extract_with_7z(zip_path, extract_dir):
    """使用7z解压文件"""
    if not os.path.exists("7z.exe") or not os.path.exists("7z.dll"):
        print("\n未找到7z.exe或7z.dll，无法解压文件")
        return False
    
    # 确保输出目录存在
    os.makedirs(extract_dir, exist_ok=True)
    
    # 构建7z命令
    cmd = [
        "7z.exe", "x", 
        f"-o{extract_dir}", 
        "-y",  # 自动确认
        zip_path
    ]
    
    try:
        print(f"\n解压中: {os.path.basename(zip_path)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"已解压: {os.path.basename(zip_path)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n解压失败: {e.stderr}")
        return False

def calculate_natives_size(version_details):
    """计算natives文件总大小"""
    os_name = get_os()
    if not os_name:
        return 0
    
    libraries = version_details.get("libraries", [])
    total_size = 0
    
    for lib in libraries:
        if "natives" in lib and "downloads" in lib and "classifiers" in lib["downloads"]:
            if os_name not in lib["natives"]:
                continue
                
            classifier = lib["natives"][os_name].replace("${arch}", "64")
            if classifier in lib["downloads"]["classifiers"]:
                total_size += lib["downloads"]["classifiers"][classifier]["size"]
    
    return total_size

def download_natives(version_details, minecraft_dir, version_id):
    """下载并解压natives文件"""
    print("\n===== 开始处理本地库文件 =====")
    
    os_name = get_os()
    if not os_name:
        print("无法识别操作系统，跳过natives下载")
        return False
    
    # 目标目录
    natives_dir = os.path.join(minecraft_dir, "versions", version_id, "natives")
    
    # 清空现有natives目录
    if os.path.exists(natives_dir):
        rmtree(natives_dir, ignore_errors=True)
    
    libraries = version_details.get("libraries", [])
    success = True
    
    for lib in libraries:
        # 检查是否为natives且与当前系统匹配
        if "natives" in lib and "downloads" in lib and "classifiers" in lib["downloads"]:
            # 检查操作系统匹配性
            if os_name not in lib["natives"]:
                continue
                
            # 获取对应的natives分类器
            classifier = lib["natives"][os_name].replace("${arch}", "64")
            if classifier not in lib["downloads"]["classifiers"]:
                continue
                
            # 下载natives压缩包
            native_info = lib["downloads"]["classifiers"][classifier]
            native_path = os.path.join(minecraft_dir, "libraries", native_info["path"])
            
            if download_file(native_info["url"], native_path):
                # 解压到natives目录
                if not extract_with_7z(native_path, natives_dir):
                    success = False
            else:
                success = False
    
    if success:
        print("\n===== 本地库文件处理完成 =====")
    return success

def calculate_libraries_size(version_details):
    """计算库文件总大小"""
    total_size = 0
    libraries = version_details.get("libraries", [])
    
    for lib in libraries:
        if "downloads" in lib and "artifact" in lib["downloads"]:
            total_size += lib["downloads"]["artifact"]["size"]
    
    return total_size

def download_libraries(version_details, minecraft_dir):
    """下载库文件"""
    print("\n===== 开始下载库文件 =====")
    
    libraries_dir = os.path.join(minecraft_dir, "libraries")
    libraries = version_details.get("libraries", [])
    total = len(libraries)
    success_count = 0
    
    for i, lib in enumerate(libraries, 1):
        if i % 10 == 0:  # 每10个库文件显示一次状态
            print(f"\n处理库文件 {i}/{total}")
            
        if "downloads" in lib and "artifact" in lib["downloads"]:
            artifact = lib["downloads"]["artifact"]
            lib_path = os.path.join(libraries_dir, artifact["path"])
            
            if download_file(artifact["url"], lib_path):
                success_count += 1
    
    print(f"\n===== 库文件下载完成: {success_count}/{total} =====")
    return success_count > 0

def calculate_assets_size(version_details, minecraft_dir):
    """计算资源文件总大小"""
    assets_dir = os.path.join(minecraft_dir, "assets")
    indexes_dir = os.path.join(assets_dir, "indexes")
    
    os.makedirs(indexes_dir, exist_ok=True)
    
    # 下载资源索引
    assets_index = version_details["assetIndex"]
    index_file = f"{assets_index['id']}.json"
    index_path = os.path.join(indexes_dir, index_file)
    
    # 先下载索引文件
    try:
        with requests.get(assets_index["url"], stream=True) as r:
            r.raise_for_status()
            with open(index_path, 'wb') as f:
                f.write(r.content)
    except Exception as e:
        print(f"资源索引预下载失败: {e}")
        return 0
    
    # 加载资源索引计算总大小
    try:
        with open(index_path, 'r') as f:
            assets_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"解析资源索引失败: {e}")
        return 0
    
    # 加上索引文件本身的大小
    total_size = assets_index["size"]
    
    # 计算所有资源对象的大小
    objects = assets_data.get("objects", {})
    for name, obj_info in objects.items():
        total_size += obj_info["size"]
    
    return total_size

def download_assets(version_details, minecraft_dir):
    """下载资源文件"""
    print("\n===== 开始下载资源文件 =====")
    
    assets_dir = os.path.join(minecraft_dir, "assets")
    objects_dir = os.path.join(assets_dir, "objects")
    indexes_dir = os.path.join(assets_dir, "indexes")
    
    os.makedirs(objects_dir, exist_ok=True)
    os.makedirs(indexes_dir, exist_ok=True)
    
    # 下载资源索引
    assets_index = version_details["assetIndex"]
    index_file = f"{assets_index['id']}.json"
    index_path = os.path.join(indexes_dir, index_file)
    
    if not download_file(assets_index["url"], index_path):
        print("\n资源索引下载失败")
        return False
    
    # 加载资源索引
    try:
        with open(index_path, 'r') as f:
            assets_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n解析资源索引失败: {e}")
        return False
    
    # 下载资源对象
    objects = assets_data.get("objects", {})
    total = len(objects)
    success_count = 0
    
    print(f"发现 {total} 个资源文件")
    
    for i, (name, obj_info) in enumerate(objects.items(), 1):
        if i % 100 == 0:  # 每100个资源显示一次状态
            print(f"\n处理资源文件 {i}/{total}")
            
        hash_val = obj_info["hash"]
        obj_path = os.path.join(objects_dir, hash_val[:2], hash_val)
        obj_url = f"https://resources.download.minecraft.net/{hash_val[:2]}/{hash_val}"
        
        # 检查文件是否已存在且哈希正确
        if os.path.exists(obj_path):
            with open(obj_path, 'rb') as f:
                if hashlib.sha1(f.read()).hexdigest() == hash_val:
                    success_count += 1
                    continue
        
        if download_file(obj_url, obj_path):
            success_count += 1
    
    print(f"\n===== 资源文件下载完成: {success_count}/{total} =====")
    return success_count > 0

def calculate_client_size(version_info, version_details):
    """计算客户端文件总大小"""
    # 版本JSON文件大小
    try:
        response = requests.head(version_info["url"])
        json_size = int(response.headers.get('content-length', 0))
    except:
        json_size = 0
        
    # 客户端JAR文件大小
    jar_size = version_details["downloads"]["client"]["size"]
    
    return json_size + jar_size

def download_client(version_info, version_details, minecraft_dir):
    """下载客户端JAR和JSON文件"""
    print("\n===== 开始下载客户端文件 =====")
    
    version_id = version_info["id"]
    versions_dir = os.path.join(minecraft_dir, "versions", version_id)
    os.makedirs(versions_dir, exist_ok=True)
    
    # 下载版本JSON
    json_path = os.path.join(versions_dir, f"{version_id}.json")
    if not download_file(version_info["url"], json_path):
        return False
    
    # 下载客户端JAR
    client_url = version_details["downloads"]["client"]["url"]
    client_path = os.path.join(versions_dir, f"{version_id}.jar")
    if not download_file(client_url, client_path):
        return False
    
    print("\n===== 客户端文件下载完成 =====")
    return True

def download_minecraft(version):
    """下载完整的Minecraft版本"""
    global total_download_size, downloaded_size
    
    # 重置进度变量
    total_download_size = 0
    downloaded_size = 0
    
    # 获取版本信息
    print("获取版本清单...")
    manifest = get_version_manifest()
    if not manifest:
        return False
    
    print(f"查找版本 {version}...")
    version_info = find_version_info(manifest, version)
    if not version_info:
        return False
    
    print(f"找到版本: {version_info['id']} ({version_info['type']})")
    
    # 获取版本详情
    print("获取版本详细信息...")
    version_details = get_version_details(version_info)
    if not version_details:
        return False
    
    # 基础目录
    minecraft_dir = os.path.join(os.getcwd(), ".minecraft")
    print(f"文件将保存到: {minecraft_dir}")
    
    # 预先计算总下载大小
    print("\n计算总下载大小...")
    total_download_size = 0
    
    # 客户端文件大小
    client_size = calculate_client_size(version_info, version_details)
    total_download_size += client_size
    print(f"客户端文件: {format_size(client_size)}")
    
    # 库文件大小
    libraries_size = calculate_libraries_size(version_details)
    total_download_size += libraries_size
    print(f"库文件: {format_size(libraries_size)}")
    
    # 资源文件大小
    assets_size = calculate_assets_size(version_details, minecraft_dir)
    total_download_size += assets_size
    print(f"资源文件: {format_size(assets_size)}")
    
    # Natives文件大小
    natives_size = calculate_natives_size(version_details)
    total_download_size += natives_size
    print(f"本地库文件: {format_size(natives_size)}")
    
    print(f"总下载大小: {format_size(total_download_size)}")
    print("开始下载...")
    
    # 依次下载各个组件
    if not download_client(version_info, version_details, minecraft_dir):
        return False
        
    if not download_libraries(version_details, minecraft_dir):
        return False
        
    if not download_assets(version_details, minecraft_dir):
        return False
        
    if not download_natives(version_details, minecraft_dir, version_info["id"]):
        return False
    
    print(f"\n===== Minecraft {version_info['id']} 已完整下载 =====")
    return True

def main():
    parser = argparse.ArgumentParser(description='Minecraft版本下载器')
    parser.add_argument('version', help='要下载的Minecraft版本，使用"latest"下载最新正式版')
    args = parser.parse_args()
    
    download_minecraft(args.version)

if __name__ == "__main__":
    main()
