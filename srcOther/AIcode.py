import argparse
import requests
import os
import json
import time
import hashlib
from urllib.parse import urlparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# -------------------------- 基础配置（未改动） --------------------------
DOWNLOAD_SOURCES = {
    "default": [  # 版本元数据、客户端JAR、依赖库（libraries）
        "https://bmclapi2.bangbang93.com",
        "https://bmclapi.bangbang93.com"
    ],
    "assets": [  # 仅资产文件（索引+对象）
        "https://bmclapi2.bangbang93.com",
        "https://bmclapi.bangbang93.com"
    ]
}

DEFAULT_MC_ROOT = Path.cwd() / ".minecraft"
VERSIONS_RECORD = Path("versions.txt")

# -------------------------- 工具函数（新增：自定义进度条核心） --------------------------
def format_size(size: int) -> str:
    """格式化文件大小（B/KB/MB/GB）"""
    if not isinstance(size, int):
        size = int(size)
    units = ["B", "KB", "MB", "GB"]
    if size == 0:
        return "0.00 B"
    idx = 0
    while size >= 1024 and idx < 3:
        size = size / 1024  # 保留小数，不做整除
        idx += 1
    return f"{size:.2f} {units[idx]}"

def calc_sha1(file_path: str or Path) -> str:
    """计算SHA1哈希（未改动）"""
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        chunk = f.read(4096)
        while chunk:
            sha1.update(chunk)
            chunk = f.read(4096)
    return sha1.hexdigest()

def get_remote_file_size(url: str) -> int:
    """获取远程文件大小（用于预统计总进度），失败返回0"""
    try:
        resp = requests.head(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"},
            allow_redirects=True
        )
        resp.raise_for_status()
        return int(resp.headers.get("content-length", 0))
    except Exception:
        return 0

def print_progress_bar(current: float, total: float, desc: str, unit: str = "") -> None:
    """
    打印自定义进度条
    :param current: 当前进度
    :param total: 总进度
    :param desc: 进度条描述（如“全局下载进度”）
    :param unit: 单位（如“个”“MB”）
    """
    # 处理总进度为0的情况（避免除以零）
    if total == 0:
        percent = 100.0
        filled_length = 20  # 进度条总长度（字符数）
    else:
        percent = (current / total) * 100
        filled_length = int(20 * current // total)  # 已填充长度
    
    # 进度条样式：[=====     ] 50.0% | 描述 | 当前/总 单位
    bar = "=" * filled_length + " " * (20 - filled_length)
    if unit:
        progress_text = f"{current:.0f}/{total:.0f} {unit}"  # 数量/大小带单位
    else:
        progress_text = f"{current:.0f}/{total:.0f}"
    
    # 用\r覆盖行首，end=''不换行，flush=True强制刷新
    print(f"\r[{bar}] {percent:5.1f}% | {desc} | {progress_text}", end="", flush=True)

# -------------------------- 源检测（仅执行一次，未改动核心逻辑） 

--------------------------
def is_source_valid(source_url: str, test_path: str) -> bool:
    try:
        test_url = f"{source_url.rstrip('/')}/{test_path.lstrip('/')}"
        resp = requests.get(
            test_url,
            stream=True,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"},
            allow_redirects=True
        )
        valid = 200 <= resp.status_code < 400
        resp.close()
        return valid
    except (requests.Timeout, requests.ConnectionError):
        return False
    except:
        return True

def get_valid_sources_once(source_type: str, test_path: str) -> List[str]:
    all_sources = DOWNLOAD_SOURCES.get(source_type, [])
    valid_sources = []
    
    print(f"\n[检测 {source_type} 源有效性（仅一次）]")
    for src in all_sources:
        if is_source_valid(src, test_path):
            valid_sources.append(src)
            print(f"✅ 有效: {src}")
        else:
            print(f"❌ 无效: {src}（超时/连接失败）")
    
    if not valid_sources:
        raise RuntimeError(f"没有检测到可用的{source_type}源")
    return valid_sources

# -------------------------- 下载函数（修改：自定义单文件进度条） 

--------------------------
def download(
    url: str, 
    save_dir: str or Path, 
    filename: Optional[str] = None, 
    expected_sha1: Optional[str] = None,
    show_progress: bool = True
) -> int:
    """通用下载：返回实际下载的文件大小（已存在返回0），自带单文件进度条"""
    try:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # 确定文件名
        if not filename:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"file_{int(time())}.dat"
        
        file_path = save_dir / filename
        
        # 跳过已存在且校验通过的文件（返回0）
        if file_path.exists():
            if expected_sha1 and calc_sha1(file_path) == expected_sha1:
                print(f"✅ {filename} 已存在且校验通过，跳过")
                return 0
            elif not expected_sha1:
                print(f"✅ {filename} 已存在，跳过")
                return 0
        
        # 开始下载
        start_time = time.time()
        response = requests.get(
            url, 
            stream=True, 
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
        )
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        # 单文件进度条（仅在需要显示时启用）
        if show_progress and total_size > 0:
            print(f"\n开始下载: {filename}")
        
        with open(file_path, 'wb') as f:
            chunk = response.raw.read(8192)
            while chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                # 实时更新单文件进度
                if show_progress and total_size > 0:
                    print_progress_bar(
                        current=downloaded_size,
                        total=total_size,
                        desc=f"单文件进度",
                        unit="B"
                    )
                chunk = response.raw.read(8192)
        
        # 单文件下载完成：换行（避免覆盖进度条）
        if show_progress and total_size > 0:
            print()  # 进度条后换行
            print(f"✅ {filename} 下载完成（{format_size(downloaded_size)}）")
        
        # SHA1校验（失败删除文件，返回0）
        if expected_sha1:
            actual_sha1 = calc_sha1(file_path)
            if actual_sha1 != expected_sha1:
                os.remove(file_path)
                raise ValueError(f"SHA1不匹配：预期{expected_sha1[:8]}... 实际{actual_sha1

[:8]}...")
            print(f"✅ {filename} 校验通过")
        
        return downloaded_size  # 返回实际下载大小
    
    except Exception as e:
        print(f"\n❌ 下载 {filename} 失败: {str(e)[:100]}")
        if os.path.exists(file_path):
            os.remove(file_path)
        raise

# -------------------------- 资产下载（修改：接收预检测源，返回大小） 

--------------------------
def download_assets(
    asset_type: str, 
    save_dir: str or Path, 
    valid_sources: List[str],  # 接收预检测好的有效源
    **kwargs
) -> Tuple[str, int]:
    """统一下载：返回文件路径 + 下载大小（未改动核心逻辑）"""
    for source in valid_sources:
        try:
            if asset_type == "client":
                version = kwargs["version"]
                url = f"{source}/version/{version}/client"
                size = download(url, save_dir, f"{version}.jar", kwargs.get("sha1"))
                return (str(save_dir / f"{version}.jar"), size)
            
            elif asset_type == "version_json":
                version = kwargs["version"]
                url = f"{source}/version/{version}/json"
                size = download(url, save_dir, f"{version}.json", kwargs.get("sha1"))
                return (str(save_dir / f"{version}.json"), size)
            
            elif asset_type == "library":
                url = kwargs["url"]
                filename = os.path.basename(urlparse(url).path)
                lib_dir = save_dir
                size = download(url, lib_dir, filename, kwargs.get("sha1"))
                return (str(lib_dir / filename), size)
            
            elif asset_type == "asset_index":
                index_id = kwargs["index_id"]
                url = f"{source}/assets/indexes/{index_id}.json"
                size = download(url, save_dir, f"{index_id}.json", kwargs.get("sha1"))
                return (str(save_dir / f"{index_id}.json"), size)
            
            elif asset_type == "asset_object":
                asset_hash = kwargs["hash"]
                url = f"{source}/objects/{asset_hash[:2]}/{asset_hash}"
                save_subdir = save_dir / asset_hash[:2]
                # 资产对象数量多，不显示单文件进度（避免刷屏）
                size = download(url, save_subdir, asset_hash, asset_hash, 

show_progress=False)
                return (str(save_subdir / asset_hash), size)
            
            else:
                raise ValueError(f"不支持的资源类型: {asset_type}")
                
        except Exception as e:
            print(f"⚠️ 源 {source} 失败，尝试下一个...")
            continue
    
    raise RuntimeError(f"所有源下载失败，资源类型: {asset_type}")

# -------------------------- 核心逻辑（修改：自定义全局双进度条） 

--------------------------
def download_minecraft_version(version: str, mc_root: str or Path = None, force: bool = 

False):
    mc_root = Path(mc_root) if mc_root else DEFAULT_MC_ROOT
    print(f"=== 开始下载 Minecraft {version} 到 {mc_root} ===")
    
    # -------------------------- 1. 仅检测一次源（关键：未改动） --------------------------
    valid_default_sources = get_valid_sources_once("default", "version/1.8.9/json")
    valid_assets_sources = get_valid_sources_once("assets", "assets/indexes/1.12.json")
    
    # -------------------------- 2. 初始化目录（未改动） --------------------------
    versions_dir = mc_root / "versions" / version
    libraries_dir = mc_root / "libraries"
    assets_index_dir = mc_root / "assets" / "indexes"
    assets_objects_dir = mc_root / "assets" / "objects"
    versions_dir.mkdir(parents=True, exist_ok=True)
    libraries_dir.mkdir(parents=True, exist_ok=True)
    assets_index_dir.mkdir(parents=True, exist_ok=True)
    assets_objects_dir.mkdir(parents=True, exist_ok=True)
    
    # -------------------------- 3. 预统计全局下载量（未改动核心逻辑） 

--------------------------
    print("\n[预统计下载资源（计算总进度）]")
    total_count = 0  # 总需下载资源数量
    total_size = 0   # 总需下载资源大小（字节）
    version_data = None
    
    # 3.1 统计：版本JSON
    version_json_path = versions_dir / f"{version}.json"
    need_download_json = force or not version_json_path.exists()
    if need_download_json:
        test_url = f"{valid_default_sources[0]}/version/{version}/json"
        json_size = get_remote_file_size(test_url)
        total_count += 1
        total_size += json_size
        print(f"- 版本JSON: 需下载（{format_size(json_size)}）")
    else:
        print(f"- 版本JSON: 已存在（跳过）")
        with open(version_json_path, "r", encoding="utf-8") as f:
            version_data = json.load(f)
    
    # 3.2 统计：客户端JAR
    client_size = 0
    if not version_data and need_download_json:
        temp_json_url = f"{valid_default_sources[0]}/version/{version}/json"
        temp_json = requests.get(temp_json_url, timeout=10).json()
        client_url = f"{valid_default_sources[0]}/version/{version}/client"
        client_size = get_remote_file_size(client_url)
    elif version_data:
        client_url = f"{valid_default_sources[0]}/version/{version}/client"
        client_size = get_remote_file_size(client_url)
    
    client_jar_path = versions_dir / f"{version}.jar"
    need_download_client = force or not client_jar_path.exists()
    if need_download_client:
        total_count += 1
        total_size += client_size
        print(f"- 客户端JAR: 需下载（{format_size(client_size)}）")
    else:
        print(f"- 客户端JAR: 已存在（跳过）")
    
    # 3.3 统计：依赖库
    lib_count = 0
    lib_total_size = 0
    if not version_data:
        temp_json_url = f"{valid_default_sources[0]}/version/{version}/json"
        version_data = requests.get(temp_json_url, timeout=10).json()
    
    for lib in version_data.get("libraries", []):
        artifact = lib.get("downloads", {}).get("artifact")
        if not artifact:
            continue
        
        lib_path = libraries_dir / artifact["path"]
        need_download_lib = force or not lib_path.exists()
        if need_download_lib:
            lib_size = get_remote_file_size(artifact["url"])
            lib_count += 1
            lib_total_size += lib_size
    
    total_count += lib_count
    total_size += lib_total_size
    print(f"- 依赖库: 需下载 {lib_count} 个（共 {format_size(lib_total_size)}）")
    
    # 3.4 统计：资产索引
    asset_index_size = 0
    asset_index = version_data.get("assetIndex", {})
    need_download_index = False
    if asset_index:
        index_id = asset_index["id"]
        index_path = assets_index_dir / f"{index_id}.json"
        need_download_index = force or not index_path.exists()
        if need_download_index:
            index_url = f"{valid_assets_sources[0]}/assets/indexes/{index_id}.json"
            asset_index_size = get_remote_file_size(index_url)
            total_count += 1
            total_size += asset_index_size
            print(f"- 资产索引: 需下载（{format_size(asset_index_size)}）")
        else:
            print(f"- 资产索引: 已存在（跳过）")
    else:
        print(f"- 资产索引: 无（跳过）")
    
    # 3.5 统计：资产对象
    asset_obj_count = 0
    asset_obj_total_size = 0
    if asset_index:
        index_id = asset_index["id"]
        index_path = assets_index_dir / f"{index_id}.json"
        if index_path.exists() and not need_download_index:
            with open(index_path, "r", encoding="utf-8") as f:
                assets_data = json.load(f)
        else:
            temp_index_url = f"{valid_assets_sources[0]}/assets/indexes/{index_id}.json"
            assets_data = requests.get(temp_index_url, timeout=10).json()
        
        for name, obj_info in assets_data.get("objects", {}).items():
            obj_hash = obj_info["hash"]
            obj_path = assets_objects_dir / obj_hash[:2] / obj_hash
            need_download_obj = force or not obj_path.exists()
            if need_download_obj:
                asset_obj_count += 1
                asset_obj_total_size += obj_info["size"]
    
    total_count += asset_obj_count
    total_size += asset_obj_total_size
    print(f"- 资产对象: 需下载 {asset_obj_count} 个（共 {format_size(asset_obj_total_size)}

）")
    print(f"\n[统计完成] 共需下载 {total_count} 个资源（总大小: {format_size(total_size)}）

")

    # -------------------------- 4. 初始化全局进度（关键：自定义双进度条） 

--------------------------
    current_count = 0  # 当前完成资源个数
    current_size = 0   # 当前完成资源大小（字节）
    print("\n" + "="*80)  # 分隔线，区分统计和下载阶段

    # -------------------------- 5. 开始下载（关联全局进度更新） --------------------------
    try:
        # 5.1 下载版本JSON
        if need_download_json:
            _, json_size = download_assets(
                "version_json", versions_dir, valid_default_sources, version=version
            )
            current_count += 1
            current_size += json_size
            # 更新全局进度条（个数+大小）
            print_progress_bar(current_count, total_count, "全局进度（个数）", "个")
            print_progress_bar(current_size, total_size, "全局进度（大小）", "B")
            # 重新读取版本元数据
            with open(version_json_path, "r", encoding="utf-8") as f:
                version_data = json.load(f)
        else:
            current_count += 1
            print_progress_bar(current_count, total_count, "全局进度（个数）", "个")
            print_progress_bar(current_size, total_size, "全局进度（大小）", "B")

        # 5.2 下载客户端JAR
        if need_download_client:
            client_info = version_data["downloads"]["client"]
            _, client_size = download_assets(
                "client", versions_dir, valid_default_sources,
                version=version, sha1=client_info["sha1"]
            )
            current_count += 1
            current_size += client_size
            print_progress_bar(current_count, total_count, "全局进度（个数）", "个")
            print_progress_bar(current_size, total_size, "全局进度（大小）", "B")
        else:
            current_count += 1
            print_progress_bar(current_count, total_count, "全局进度（个数）", "个")
            print_progress_bar(current_size, total_size, "全局进度（大小）", "B")

        # 5.3 下载依赖库
        print("\n\n=== 开始下载依赖库 ===")
        for lib in version_data.get("libraries", []):
            artifact = lib.get("downloads", {}).get("artifact")
            if not artifact:
                continue
            
            lib_path = libraries_dir / artifact["path"]
            need_download_lib = force or not lib_path.exists()
            if need_download_lib:
                try:
                    _, lib_size = download_assets(
                        "library", os.path.dirname(lib_path), valid_default_sources,
                        url=artifact["url"], sha1=artifact.get("sha1")
                    )
                    current_count += 1
                    current_size += lib_size
                except Exception as e:
                    print(f"⚠️ 库 {os.path.basename(lib_path)} 下载失败: {str(e)}, 继续下

一个")
                    current_count += 1  # 失败也计数（避免进度卡住）
            else:
                current_count += 1
            
            # 每次处理后更新全局进度
            print_progress_bar(current_count, total_count, "全局进度（个数）", "个")
            print_progress_bar(current_size, total_size, "全局进度（大小）", "B")

        # 5.4 下载资产索引
        if asset_index and need_download_index:
            print("\n\n=== 开始下载资产索引 ===")
            try:
                _, index_size = download_assets(
                    "asset_index", assets_index_dir, valid_assets_sources,
                    index_id=asset_index["id"], sha1=asset_index.get("sha1")
                )
                current_count += 1
                current_size += index_size
                # 读取资产索引（用于下载对象）
                with open(assets_index_dir / f"{asset_index['id']}.json", "r", 

encoding="utf-8") as f:
                    assets_data = json.load(f)
            except Exception as e:
                print(f"⚠️ 资产索引下载失败: {str(e)}")
                current_count += 1
        elif asset_index:
            # 读取已存在的资产索引
            with open(assets_index_dir / f"{asset_index['id']}.json", "r", encoding="utf-

8") as f:
                assets_data = json.load(f)
            current_count += 1
        
        # 更新资产索引后的全局进度
        print_progress_bar(current_count, total_count, "全局进度（个数）", "个")
        print_progress_bar(current_size, total_size, "全局进度（大小）", "B")

        # 5.5 下载资产对象
        if asset_index and 'assets_data' in locals():
            print("\n\n=== 开始下载资产对象 ===")
            objects = assets_data.get("objects", {})
            for name, obj_info in objects.items():
                obj_hash = obj_info["hash"]
                obj_path = assets_objects_dir / obj_hash[:2] / obj_hash
                need_download_obj = force or not obj_path.exists()
                
                if need_download_obj:
                    try:
                        _, obj_size = download_assets(
                            "asset_object", assets_objects_dir, valid_assets_sources,
                            hash=obj_hash
                        )
                        current_size += obj_size
                    except Exception as e:
                        print(f"⚠️ 资产 {name} 下载失败: {str(e)}")
                current_count += 1  # 无论成功/失败都计数
                
                # 每处理10个资产对象更新一次进度（避免频繁刷新）
                if current_count % 10 == 0 or current_count == total_count:
                    print_progress_bar(current_count, total_count, "全局进度（个数）", 

"个")
                    print_progress_bar(current_size, total_size, "全局进度（大小）", "B")

    finally:
        # 确保进度条最终显示100%（处理异常情况）
        print_progress_bar(min(current_count, total_count), total_count, "全局进度（个

数）", "个")
        print_progress_bar(min(current_size, total_size), total_size, "全局进度（大小）", 

"B")
        print("\n" + "="*80)  # 分隔线，标记下载阶段结束

    # -------------------------- 6. 记录版本（未改动） --------------------------
    with open(VERSIONS_RECORD, "a+", encoding="utf-8") as f:
        f.seek(0)
        if version not in f.read():
            f.write(f"{version} | {time.strftime('%Y-%m-%d %H:%M:%S')} | {mc_root}\n")
    
    print(f"\n🎉 Minecraft {version} 下载完成！")
    print(f"路径: {mc_root}")

# -------------------------- 命令行入口（未改动） --------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minecraft下载工具（单次源检测+自定义进度

条）")
    parser.add_argument("--download", metavar="VERSION", required=True, help="版本（如1.8.9

、1.12.2）")
    parser.add_argument("--path", help=f"保存路径（默认: {DEFAULT_MC_ROOT}）")
    parser.add_argument("--force", action="store_true", help="强制重新下载")
    
    args = parser.parse_args()
    
    try:
        download_minecraft_version(args.download, args.path, args.force)
    except Exception as e:
        print(f"\n❌ 操作失败: {str(e)}")
        exit(1)
