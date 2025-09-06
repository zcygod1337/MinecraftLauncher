import os
import json
import requests
from urllib.parse import urlparse

# BMCLAPI base URL
BMCLAPI_BASE = "https://bmclapi2.bangbang93.com"

def download(url, path, filename=None, show_progress=True):
    """Download a file from a URL to a specified path with optional filename."""
    try:
        # If filename is not provided, try to extract it from the URL or Content-Disposition header
        if filename is None:
            # Try to get filename from URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # If that doesn't work, try Content-Disposition header
            if not filename or '.' not in filename:
                response = requests.head(url)
                if "Content-Disposition" in response.headers:
                    content_disposition = response.headers["Content-Disposition"]
                    if "filename=" in content_disposition:
                        filename = content_disposition.split("filename=")[-1].strip('"')
                    else:
                        filename = "default_filename"
                else:
                    filename = "default_filename"
        
        # Ensure the path exists
        os.makedirs(path, exist_ok=True)
        
        # Full path to save the file
        file_path = os.path.join(path, filename)
        
        # If the file already exists, skip downloading
        if os.path.exists(file_path):
            print(f"File {filename} already exists. Skipping download.")
            return file_path
        
        # Download the file with streaming
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Get total file size if available
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        # Write the content to file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Show progress if requested
                    if show_progress and total_size > 0:
                        percent = (downloaded_size / total_size) * 100
                        print(f"\rDownloading {filename}: {percent:.1f}% ({downloaded_size}/{total_size} bytes)", end='')
        
        if show_progress:
            print()  # New line after progress
        
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def download_minecraft_client(version, path, show_progress=True):
    """Download Minecraft client jar for a specific version."""
    url = f"{BMCLAPI_BASE}/version/{version}/client"
    return download(url, path, f"{version}.jar", show_progress)

def download_minecraft_server(version, path, show_progress=True):
    """Download Minecraft server jar for a specific version."""
    url = f"{BMCLAPI_BASE}/version/{version}/server"
    return download(url, path, f"minecraft_server.{version}.jar", show_progress)

def download_assets_index(version, path, show_progress=True):
    """Download assets index JSON for a specific version."""
    url = f"{BMCLAPI_BASE}/version/{version}/json"
    return download(url, path, f"{version}.json", show_progress)

def download_asset_object(hash, path, show_progress=True):
    """Download a specific asset object by its hash."""
    # The hash is split into two parts for the URL path
    hash_prefix = hash[:2]
    url = f"{BMCLAPI_BASE}/objects/{hash_prefix}/{hash}"
    return download(url, path, hash, show_progress)

def download_assets(asset_type, path, **kwargs):
    """
    Unified function to download different types of Minecraft assets.
    
    Args:
        asset_type (str): Type of asset to download. Options:
            - "client": Minecraft client jar
            - "server": Minecraft server jar
            - "assets_index": Assets index JSON
            - "asset_object": Specific asset object by hash
            - "url": Direct URL download (requires 'url' in kwargs)
        path (str): Directory path to save the downloaded file
        **kwargs: Additional arguments based on asset_type:
            For "client", "server", "assets_index": 
                - version (str): Minecraft version
            For "asset_object":
                - hash (str): Asset hash
            For "url":
                - url (str): Direct URL to download
                - filename (str, optional): Filename for the downloaded file
    
    Returns:
        str: Path to the downloaded file
    """
    if asset_type == "client":
        if "version" not in kwargs:
            raise ValueError("Missing 'version' argument for client download")
        return download_minecraft_client(kwargs["version"], path)
    
    elif asset_type == "server":
        if "version" not in kwargs:
            raise ValueError("Missing 'version' argument for server download")
        return download_minecraft_server(kwargs["version"], path)
    
    elif asset_type == "assets_index":
        if "version" not in kwargs:
            raise ValueError("Missing 'version' argument for assets index download")
        return download_assets_index(kwargs["version"], path)
    
    elif asset_type == "asset_object":
        if "hash" not in kwargs:
            raise ValueError("Missing 'hash' argument for asset object download")
        return download_asset_object(kwargs["hash"], path)
    
    elif asset_type == "url":
        if "url" not in kwargs:
            raise ValueError("Missing 'url' argument for direct URL download")
        filename = kwargs.get("filename")
        return download(kwargs["url"], path, filename)
    
    else:
        raise ValueError(f"Unsupported asset type: {asset_type}")

def download_minecraft_dependencies(version, base_path, show_progress=True):
    """
    自动下载指定版本的所有依赖（libraries + assets）
    """
    # 下载版本的 JSON 文件
    version_json_path = download_assets("assets_index", os.path.join(base_path, "versions"), version=version)
    
    # 读取版本 JSON
    with open(version_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 下载 libraries
    lib_dir = os.path.join(base_path, "libraries")
    for lib in data.get("libraries", []):
        artifact = lib.get("downloads", {}).get("artifact")
        if artifact and "url" in artifact:
            url = artifact["url"]
            # 强制使用 BMCLAPI 的基础URL，确保下载不会被镜像站点阻止
            url = url.replace("https://mirrors.ustc.edu.cn/bmclapi", BMCLAPI_BASE)
            filename = os.path.basename(urlparse(url).path)
            download(url, lib_dir, filename, show_progress)
    
    # 检查是否存在 assets/indexes/{version}.json，如果没有则下载
    asset_index_path = os.path.join(base_path, "assets", "indexes", f"{version}.json")
    if not os.path.exists(asset_index_path):
        download_assets("assets_index", os.path.join(base_path, "assets", "indexes"), version=version)
    
    # 读取 assets index 文件
    with open(asset_index_path, "r", encoding="utf-8") as f:
        assets = json.load(f)
    
    # 检查 'objects' 键是否存在
    if "objects" in assets:
        obj_dir = os.path.join(base_path, "assets", "objects")
        for k, v in assets["objects"].items():
            h = v["hash"]
            download_asset_object(h, obj_dir, show_progress)
    else:
        print(f"Warning: 'objects' field missing in assets index for version {version}. Skipping asset object downloads.")
