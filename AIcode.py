import argparse
import requests
import subprocess
import os
import json
import time
import shutil
import hashlib
from urllib.parse import urlparse
from typing import Dict, List

# -------------------------- 全局配置 --------------------------
# 扩展下载源列表，增加更多可靠镜像
MC_DOWNLOAD_SOURCES = [
    "https://bmclapi2.bangbang93.com",
    "https://bmclapi.bangbang93.com",
    "https://api.mcbbs.net",
    "https://download.mcbbs.net",
    "https://mirror.ghproxy.com/https://raw.githubusercontent.com",
    "https://mcversions.net/downloads/asset-indexes"
]
USERNAME_FILE = ".mc_username"                       # 用户名存储文件
MC_ROOT_DIR = os.path.join(os.getcwd(), ".minecraft") # MC根目录
JAVA_ROOT_DIR = os.path.join(os.getcwd(), "java")     # Java安装根目录
VERSIONS_RECORD = "versions.txt"                      # 已下载MC版本记录文件
SEVEN_ZIP_PATH = os.path.join(os.getcwd(), "7z.exe")  # 7z.exe路径（当前文件夹）

# 资产索引文件手动下载链接（1.12.2专用）
MANUAL_ASSET_LINKS = {
    "1.12": [
        "https://mcversions.net/downloads/asset-indexes/1.12.json",
        "https://github.com/InventivetalentDev/minecraft-assets/tree/1.12.2",
        "https://legacy.curseforge.com/minecraft/assets/1.12"
    ]
}

# Java版本映射（MC版本 -> 所需Java主版本）
MC_JAVA_MAP = {
    "1.7.10": "8", "1.8.9": "8", "1.12.2": "8", "1.16.5": "8",
    "1.17.1": "16", "1.18.2": "17", "1.19.4": "17", "1.20.1": "17", "1.21": "17"
}

# Java下载链接（Windows版）
JAVA_MIRRORS = {
    "8": [
        "https://aka.ms/download-jdk/microsoft-jdk-8u392-windows-x64.zip",
        "https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u392-b08/OpenJDK8U-jre_x64_windows_hotspot_8u392b08.zip"
    ],
    "16": [
        "https://mirrors.huaweicloud.com/adoptium/16/jre/x64/windows/OpenJDK16U-jre_x64_windows_hotspot_16.0.2_7.zip"
    ],
    "17": [
        "https://mirrors.huaweicloud.com/adoptium/17/jre/x64/windows/OpenJDK17U-jre_x64_windows_hotspot_17.0.11_9.zip"
    ]
}


# -------------------------- 工具函数 --------------------------
def format_size(size_bytes: int) -> str:
    """格式化字节为易读单位（B/KB/MB/GB）"""
    units = ["B", "KB", "MB", "GB"]
    idx = 0
    while size_bytes >= 1024 and idx < 3:
        size_bytes /= 1024
        idx += 1
    return f"{size_bytes:.2f} {units[idx]}"


def native_progress_bar(current: int, total: int, filename: str):
    """原生进度条（单行刷新）"""
    if total == 0:
        print(f"下载 {filename}...")
        return
    percent = (current / total) * 100
    bar_len = 50
    completed = int(bar_len * percent / 100)
    bar = "#" * completed + " " * (bar_len - completed)
    speed = current / (time.time() - _download_start_time) if (time.time() - _download_start_time) > 0 else 0
    print(
        f"\r{filename} | [{bar}] {percent:.1f}% | 已下: {format_size(current)} | 速度: {format_size(speed)}/s",
        end="", flush=True
    )


def is_valid_archive(file_path: str) -> bool:
    """检查文件是否为有效的压缩包（7z可解压）"""
    if not os.path.exists(file_path):
        return False
    valid_exts = [".zip", ".tar.gz", ".gz", ".tar"]
    return any(file_path.lower().endswith(ext) for ext in valid_exts)


def calculate_file_hash(file_path: str) -> str:
    """计算文件的SHA-1哈希值，用于验证文件完整性（兼容旧版Python）"""
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        chunk = f.read(4096)
        while chunk:
            sha1.update(chunk)
            chunk = f.read(4096)
    return sha1.hexdigest()


# -------------------------- MC版本记录管理 --------------------------
def get_recorded_versions() -> List[str]:
    """读取versions.txt中的已下载版本（去重、去空）"""
    if not os.path.exists(VERSIONS_RECORD):
        return []
    with open(VERSIONS_RECORD, "r", encoding="utf-8") as f:
        versions = [line.strip() for line in f if line.strip()]
    return list(set(versions))  # 去重


def add_version_to_record(version: str):
    """将下载完成的MC版本添加到versions.txt（避免重复）"""
    recorded = get_recorded_versions()
    if version in recorded:
        return  # 已存在则跳过
    
    with open(VERSIONS_RECORD, "a", encoding="utf-8") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(f"{version} | 下载时间: {timestamp}\n")
    print(f"✅ 已将 {version} 记录到 {VERSIONS_RECORD}")


def sync_versions_record():
    """同步本地已下载MC版本到versions.txt（补全未记录的版本）"""
    local_versions = []
    versions_dir = os.path.join(MC_ROOT_DIR, "versions")
    if os.path.exists(versions_dir):
        for dir_name in os.listdir(versions_dir):
            dir_path = os.path.join(versions_dir, dir_name)
            if os.path.isdir(dir_path):
                jar_path = os.path.join(dir_path, f"{dir_name}.jar")
                json_path = os.path.join(dir_path, f"{dir_name}.json")
                if os.path.exists(jar_path) and os.path.exists(json_path):
                    local_versions.append(dir_name)
    
    recorded = get_recorded_versions()
    for ver in local_versions:
        if ver not in recorded:
            add_version_to_record(ver)


# -------------------------- 用户名管理 --------------------------
def set_username(username: str):
    """设置并保存用户名"""
    with open(USERNAME_FILE, "w", encoding="utf-8") as f:
        f.write(username.strip())
    print(f"✅ 用户名已设置为: {username}")


def get_username() -> str:
    """读取用户名（默认：Player）"""
    return open(USERNAME_FILE, "r", encoding="utf-8").read().strip() if os.path.exists(USERNAME_FILE) else "Player"


# -------------------------- Java管理 --------------------------
def get_required_java(mc_version: str) -> str:
    """根据MC版本获取所需Java版本（默认返回8）"""
    main_ver = mc_version.split("-")[0]
    return MC_JAVA_MAP.get(main_ver, "8")


def check_java_installed(java_ver: str) -> str:
    """检查Java是否已安装，返回可执行路径；未安装返回空"""
    java_dir = os.path.join(JAVA_ROOT_DIR, f"jre{java_ver}")
    java_exe = os.path.join(java_dir, "bin", "java.exe")  # Windows下是java.exe
    
    if os.path.exists(java_exe):
        try:
            output = subprocess.check_output([java_exe, "-version"], stderr=subprocess.STDOUT, text=True)
            if f"version \"{java_ver}" in output or f"version \"1.{java_ver}" in output:
                return java_exe
        except:
            pass
    return ""


def extract_with_7z(archive_path: str, extract_dir: str):
    """用7z.exe解压压缩包"""
    if not os.path.exists(SEVEN_ZIP_PATH):
        raise RuntimeError(f"未找到7z.exe！请确保它在当前文件夹: {SEVEN_ZIP_PATH}")
    
    os.makedirs(extract_dir, exist_ok=True)
    
    cmd = [
        SEVEN_ZIP_PATH,
        "x",  # 解压（保留目录结构）
        archive_path,
        f"-o{extract_dir}",
        "-y"
    ]
    
    try:
        print(f"📦 正在用7z解压 {os.path.basename(archive_path)}...")
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"✅ 解压完成到: {extract_dir}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"7z解压失败: {e.stderr}")


def download_java(java_ver: str):
    """下载并安装指定版本Java"""
    if java_ver not in JAVA_MIRRORS:
        raise RuntimeError(f"不支持的Java版本: {java_ver}")
    
    java_urls = JAVA_MIRRORS[java_ver]
    temp_file = os.path.join(JAVA_ROOT_DIR, f"openjdk{java_ver}.zip")
    java_target_dir = os.path.join(JAVA_ROOT_DIR, f"jre{java_ver}")

    os.makedirs(JAVA_ROOT_DIR, exist_ok=True)

    for url in java_urls:
        try:
            filename = os.path.basename(urlparse(url).path)
            global _download_start_time
            _download_start_time = time.time()
            print(f"\n📥 尝试从链接 {java_urls.index(url)+1}/{len(java_urls)} 下载Java {java_ver} ({filename})...")
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(url, stream=True, timeout=30, headers=headers, allow_redirects=True)
            resp.raise_for_status()
            
            content_type = resp.headers.get('content-type', '')
            valid_types = ['application/zip', 'application/octet-stream', 'application/x-zip-compressed']
            if not any(typ in content_type for typ in valid_types):
                print(f"⚠️  链接返回非预期内容类型: {content_type}，尝试下一个链接")
                continue
            
            total_size = int(resp.headers.get("content-length", 0))
            downloaded = 0

            with open(temp_file, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        native_progress_bar(downloaded, total_size, filename)
            
            print(f"\n✅ Java {java_ver} 下载完成")

            if not is_valid_archive(temp_file):
                print(f"⚠️  下载的文件不是有效的压缩包，尝试下一个链接")
                os.remove(temp_file)
                continue

            temp_extract = os.path.join(JAVA_ROOT_DIR, "temp_extract")
            if os.path.exists(temp_extract):
                shutil.rmtree(temp_extract)
            extract_with_7z(temp_file, temp_extract)

            if os.listdir(temp_extract):
                extract_root = os.path.join(temp_extract, os.listdir(temp_extract)[0])
                if os.path.exists(java_target_dir):
                    shutil.rmtree(java_target_dir)
                shutil.move(extract_root, java_target_dir)
                shutil.rmtree(temp_extract)
            else:
                raise RuntimeError("解压后目录为空，可能是损坏的压缩包")

            os.remove(temp_file)
            print(f"✅ Java {java_ver} 已安装到: {java_target_dir}")
            return

        except Exception as e:
            print(f"⚠️  此链接下载失败: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            continue

    raise RuntimeError(f"所有链接都无法成功下载并安装Java {java_ver}")


def get_java_exe(mc_version: str = None) -> str:
    """获取Java可执行路径"""
    if mc_version is None:
        java_ver = args.downloadjava
        java_exe = check_java_installed(java_ver)
        if java_exe:
            print(f"ℹ️ Java {java_ver} 已安装，跳过下载")
            return java_exe
        download_java(java_ver)
        return check_java_installed(java_ver)
    
    java_ver = get_required_java(mc_version)
    java_exe = check_java_installed(java_ver)
    
    if java_exe:
        print(f"ℹ️ 检测到已安装Java {java_ver}，直接使用")
        return java_exe
    
    print(f"ℹ️ 未检测到Java {java_ver}，自动下载适配版本...")
    download_java(java_ver)
    return check_java_installed(java_ver)


# -------------------------- MC资产文件下载 --------------------------
def download_with_fallback(urls, save_path):
    """尝试从多个URL下载文件，直到成功或全部失败"""
    for idx, url in enumerate(urls):
        try:
            print(f"📥 尝试从源 {idx+1}/{len(urls)} 下载: {os.path.basename(save_path)}")
            global _download_start_time
            _download_start_time = time.time()
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(url, stream=True, timeout=15, headers=headers)
            resp.raise_for_status()
            
            total_size = int(resp.headers.get("content-length", 0))
            downloaded = 0

            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        native_progress_bar(downloaded, total_size, os.path.basename(save_path))
            
            print(f"\n✅ 下载完成: {os.path.basename(save_path)}")
            return True
        except Exception as e:
            print(f"⚠️  源 {idx+1} 下载失败: {str(e)}")
            if os.path.exists(save_path):
                os.remove(save_path)
            continue
    
    return False


def prompt_manual_download(asset_index: str):
    """提示用户手动下载资产索引文件"""
    print("\n📋 请手动下载资产索引文件:")
    print(f"所需文件: {asset_index}.json")
    
    # 显示推荐下载链接
    print("\n推荐下载链接:")
    for i, link in enumerate(MANUAL_ASSET_LINKS.get(asset_index, []), 1):
        print(f"{i}. {link}")
    
    # 显示保存路径
    save_dir = os.path.join(MC_ROOT_DIR, "assets", "indexes")
    save_path = os.path.join(save_dir, f"{asset_index}.json")
    print(f"\n下载后请保存到以下路径:")
    print(f"📂 {save_path}")
    
    # 等待用户确认
    input("\n请完成手动下载并按回车键继续...")
    
    # 验证文件是否存在
    if not os.path.exists(save_path):
        raise RuntimeError(f"未在 {save_path} 找到文件，请检查路径是否正确")
    print("✅ 检测到手动下载的文件，继续处理...")


def download_mc_assets(version: str, assets_index: str):
    """下载MC所需的资产文件（纹理、声音等），支持手动下载备选"""
    assets_dir = os.path.join(MC_ROOT_DIR, "assets")
    objects_dir = os.path.join(assets_dir, "objects")
    indexes_dir = os.path.join(assets_dir, "indexes")
    
    # 创建资产目录
    os.makedirs(objects_dir, exist_ok=True)
    os.makedirs(indexes_dir, exist_ok=True)
    
    # 构建多个源的资产索引文件URL
    index_urls = [
        f"{source}/assets/indexes/{assets_index}.json" 
        for source in MC_DOWNLOAD_SOURCES
    ]
    # 1.12.2特殊处理 - 尝试不同的路径格式
    if assets_index == "1.12":
        index_urls.extend([
            f"{source}/minecraft/assets/indexes/{assets_index}.json" 
            for source in MC_DOWNLOAD_SOURCES
        ])
        index_urls.extend([
            f"{source}/1.12.json" 
            for source in MC_DOWNLOAD_SOURCES if "mcversions.net" in source or "github.com" in source
        ])
    
    index_path = os.path.join(indexes_dir, f"{assets_index}.json")
    
    # 先检查是否已有文件
    if os.path.exists(index_path):
        print(f"ℹ️ 资产索引文件 {assets_index}.json 已存在，跳过下载")
    else:
        # 尝试自动下载
        print(f"\n📥 开始下载资产索引文件 {assets_index}.json...")
        if not download_with_fallback(index_urls, index_path):
            # 自动下载失败，提示手动下载
            print("❌ 自动下载失败，将引导您手动下载")
            prompt_manual_download(assets_index)
    
    # 解析索引并下载资产对象
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            index_data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"解析资产索引文件失败: {str(e)}\n请尝试重新手动下载文件")
    
    total_objects = len(index_data.get("objects", {}))
    downloaded_objects = 0
    print(f"\n📥 开始下载 {total_objects} 个资产文件（可能需要一段时间）...")
    
    for obj_hash, obj_info in index_data.get("objects", {}).items():
        # 资产文件路径规则：前2位哈希作为目录，完整哈希作为文件名
        obj_dir = os.path.join(objects_dir, obj_hash[:2])
        obj_path = os.path.join(obj_dir, obj_hash)
        
        if os.path.exists(obj_path) and os.path.getsize(obj_path) == obj_info["size"]:
            downloaded_objects += 1
            continue  # 已存在且完整，跳过
        
        # 构建多个源的资产文件URL
        obj_urls = [
            f"{source}/assets/objects/{obj_hash[:2]}/{obj_hash}" 
            for source in MC_DOWNLOAD_SOURCES
        ]
        
        try:
            os.makedirs(obj_dir, exist_ok=True)
            if download_with_fallback(obj_urls, obj_path):
                downloaded_objects += 1
            # 显示进度
            if downloaded_objects % 50 == 0:  # 每50个文件显示一次进度
                print(f"已下载 {downloaded_objects}/{total_objects} 个资产文件")
        except Exception as e:
            print(f"⚠️  资产文件 {obj_hash} 处理失败: {str(e)}")
    
    print(f"✅ 资产文件下载完成（{downloaded_objects}/{total_objects}）")


# -------------------------- MC下载 --------------------------
def get_mc_metadata(version: str) -> Dict:
    """获取MC版本元数据，支持多源切换"""
    for idx, source in enumerate(MC_DOWNLOAD_SOURCES):
        try:
            url = f"{source}/version/{version}/json"
            print(f"📥 从源 {idx+1}/{len(MC_DOWNLOAD_SOURCES)} 获取版本元数据...")
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"⚠️  源 {idx+1} 获取元数据失败: {str(e)}")
            continue
    
    raise RuntimeError(f"所有源都无法获取 {version} 的版本元数据")


def download_mc_file(version: str, file_type: str, save_path: str):
    """下载MC文件（客户端JAR等），支持多源切换"""
    file_urls = [
        f"{source}/version/{version}/{file_type}" 
        for source in MC_DOWNLOAD_SOURCES
    ]
    
    if not download_with_fallback(file_urls, save_path):
        raise RuntimeError(f"所有源都无法下载 {version} 的{file_type}文件")


def verify_mc_jar(version: str, expected_hash: str) -> bool:
    """验证MC客户端JAR文件的完整性"""
    mc_jar = os.path.join(MC_ROOT_DIR, "versions", version, f"{version}.jar")
    if not os.path.exists(mc_jar):
        return False
    
    try:
        file_hash = calculate_file_hash(mc_jar)
        return file_hash == expected_hash
    except Exception as e:
        print(f"⚠️ 验证JAR文件时出错: {str(e)}")
        return False


def download_mc(version: str, force_reinstall: bool = False):
    """下载MC指定版本（含资产文件，支持强制重新安装）"""
    mc_dir = os.path.join(MC_ROOT_DIR, "versions", version)
    mc_jar = os.path.join(mc_dir, f"{version}.jar")
    meta_path = os.path.join(mc_dir, f"{version}.json")
    
    # 获取元数据
    metadata = get_mc_metadata(version)
    expected_hash = metadata.get("downloads", {}).get("client", {}).get("sha1", "")
    
    # 强制重新安装或JAR文件不存在/损坏
    if force_reinstall or not os.path.exists(mc_jar) or (expected_hash and not verify_mc_jar(version, expected_hash)):
        print(f"\n📥 开始下载Minecraft {version}客户端...")
        
        # 删除旧文件
        if os.path.exists(mc_dir):
            shutil.rmtree(mc_dir)
        os.makedirs(mc_dir, exist_ok=True)
        
        # 下载客户端JAR
        download_mc_file(version, "client", mc_jar)
        
        # 保存版本元数据
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        # 验证下载的JAR文件
        if expected_hash and not verify_mc_jar(version, expected_hash):
            raise RuntimeError(f"Minecraft {version} JAR文件损坏，下载失败")
    else:
        print(f"ℹ️ Minecraft {version} 客户端已存在且完整，跳过下载")
    
    # 下载资产文件
    assets_index = metadata.get("assetIndex", {}).get("id")
    if assets_index:
        download_mc_assets(version, assets_index)
    else:
        print("⚠️ 未找到资产索引信息，可能导致启动失败")
        # 1.12.2特殊处理 - 手动指定资产索引
        if version in ["1.12.2", "1.12"]:
            print("💡 尝试使用1.12默认资产索引...")
            download_mc_assets(version, "1.12")
    
    add_version_to_record(version)
    print(f"✅ Minecraft {version} 准备完成（保存目录: {MC_ROOT_DIR}）")


# -------------------------- MC启动 --------------------------
def launch_mc(version: str):
    """启动MC指定版本"""
    # 1. 检查依赖
    java_exe = get_java_exe(version)
    if not java_exe:
        raise RuntimeError("Java环境配置失败，无法启动MC")
    
    mc_jar = os.path.join(MC_ROOT_DIR, "versions", version, f"{version}.jar")
    if not os.path.exists(mc_jar):
        raise RuntimeError(f"Minecraft {version} 未下载，请先执行 --download {version}")

    # 2. 启动参数
    username = get_username()
    launch_cmd = [
        java_exe,
        "-Xmx1G",
        "-Xms512M",
        "-jar", mc_jar,
        f"--username={username}",
        f"--version={version}",
        "--gameDir", MC_ROOT_DIR,
        "--assetsDir", os.path.join(MC_ROOT_DIR, "assets"),
        "--accessToken", "0"  # 离线模式
    ]

    # 3. 启动MC并显示详细输出
    print(f"\n🚀 启动Minecraft {version}（用户: {username}）...")
    print(f"📝 启动命令: {' '.join(launch_cmd)}")
    try:
        # 显示MC的启动日志和错误信息
        result = subprocess.run(
            launch_cmd,
            check=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print("✅ MC启动成功！")
        print("📝 日志:", result.stdout)
    except subprocess.CalledProcessError as e:
        # 输出详细错误日志
        print(f"❌ MC启动失败（退出码: {e.returncode}）")
        print(f"📝 错误日志:\n{e.stdout}")
        
        # 检测主类找不到错误，建议重新安装
        if "找不到或无法加载主类" in e.stdout:
            print("\n💡 检测到JAR文件可能损坏，建议执行以下命令重新安装:")
            print(f"python main.py --download {version} --force")
        
        raise RuntimeError(f"Minecraft启动失败，请查看上面的错误日志")


# -------------------------- 命令行入口 --------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minecraft全功能启动器（Windows适配版）")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--download", metavar="VERSION", help="下载指定MC版本（如1.12.2）")
    group.add_argument("--run", metavar="VERSION", help="启动指定MC版本（如1.12.2）")
    group.add_argument("--username", metavar="NAME", help="设置MC用户名（如Steve）")
    group.add_argument("--downloadjava", metavar="VERSION", help="手动下载指定Java版本（如8/17）")
    group.add_argument("--sync-versions", action="store_true", help="同步本地MC版本到versions.txt")
    
    # 强制重新安装选项
    parser.add_argument("--force", action="store_true", help="强制重新下载MC客户端文件")

    args = parser.parse_args()

    try:
        if args.username:
            set_username(args.username)
        elif args.download:
            get_java_exe(args.download)
            download_mc(args.download, args.force)
        elif args.run:
            launch_mc(args.run)
        elif args.downloadjava:
            get_java_exe()
        elif args.sync_versions:
            sync_versions_record()
            print(f"✅ 已同步本地MC版本到 {VERSIONS_RECORD}")
    except Exception as e:
        print(f"\n❌ 操作失败: {str(e)}")
        exit(1)
