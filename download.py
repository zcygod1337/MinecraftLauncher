import os
import json
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import random
import hashlib

BMCLAPI_BASE = "https://bmclapi2.bangbang93.com"

def _ensure_filename_from_url(url):
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    return name or "default_filename"

def sha1_file(file_path):
    h = hashlib.sha1()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def download(url, path, filename=None, show_progress=True, retries=5, timeout=15, expected_sha1=None):
    if filename is None:
        filename = _ensure_filename_from_url(url)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)

    if os.path.exists(file_path) and (not expected_sha1 or sha1_file(file_path) == expected_sha1):
        if show_progress:
            print(f"File {filename} already exists. Skipping.")
        return file_path

    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, stream=True, timeout=timeout, allow_redirects=True)
            resp.raise_for_status()
            total_size = int(resp.headers.get('content-length', 0) or 0)
            downloaded_size = 0
            tmp_path = file_path + ".part"
            with open(tmp_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if show_progress and total_size > 0:
                            percent = (downloaded_size / total_size) * 100
                            print(f"\rDownloading {filename}: {percent:.1f}%", end='', flush=True)
            if expected_sha1 and sha1_file(tmp_path) != expected_sha1:
                raise RuntimeError(f"SHA1 mismatch for {filename}")
            os.replace(tmp_path, file_path)
            if show_progress:
                print()
            return file_path
        except Exception as e:
            last_exc = e
            try:
                tmp = file_path + ".part"
                if os.path.exists(tmp):
                    os.remove(tmp)
            except:
                pass
            if attempt < retries:
                backoff = min(2 ** attempt, 30) + random.uniform(0, 0.5)
                print(f"\n下载失败: {url} ({e}). 重试 {attempt}/{retries}，等待 {backoff:.1f}s ...")
                time.sleep(backoff)
                continue
            else:
                print(f"\n下载失败: {url}，已用尽重试。")
                raise last_exc

def _download_worker(url, path, filename, progress_lock, progress_data, retries, timeout, expected_sha1):
    try:
        download(url, path, filename, show_progress=False, retries=retries, timeout=timeout, expected_sha1=expected_sha1)
        with progress_lock:
            progress_data['completed'] += 1
            completed = progress_data['completed']
            total = progress_data['total']
            percent = (completed / total) * 100
            print(f"\rDownloading dependencies: {completed}/{total} ({percent:.1f}%)", end="", flush=True)
    except Exception as e:
        with progress_lock:
            progress_data['completed'] += 1
            print(f"\nFailed to download {filename}: {e}")

def download_minecraft_dependencies(version, base_path, max_workers=16, retries=5, timeout=15):
    version_dir = os.path.join(base_path, "versions", version)
    version_json_path = os.path.join(version_dir, f"{version}.json")
    with open(version_json_path, "r", encoding="utf-8") as f:
        version_json = json.load(f)

    tasks = []

    asset_index_info = version_json.get("assetIndex")
    if asset_index_info:
        asset_index_url = normalize_url(asset_index_info.get("url"))
        asset_index_path = os.path.join(base_path, "assets", "indexes")
        asset_index_filename = f"{asset_index_info.get('id')}.json"
        expected_sha1 = asset_index_info.get("sha1")
        download(asset_index_url, asset_index_path, asset_index_filename, show_progress=False, retries=retries, timeout=timeout, expected_sha1=expected_sha1)

        with open(os.path.join(asset_index_path, asset_index_filename), "r", encoding="utf-8") as f:
            assets = json.load(f).get("objects", {})

        for _, obj in assets.items():
            hash_value = obj.get("hash")
            if not hash_value:
                continue
            subdir = hash_value[:2]
            url = f"{BMCLAPI_BASE}/assets/{subdir}/{hash_value}"
            path = os.path.join(base_path, "assets", "objects", subdir)
            tasks.append((url, path, hash_value, hash_value))

    for lib in version_json.get("libraries", []):
        downloads = lib.get("downloads", {})
        if downloads.get("artifact"):
            artifact = downloads["artifact"]
            url = normalize_url(artifact.get("url"))
            full_path = os.path.join(base_path, "libraries", artifact.get("path").replace("/", os.sep))
            path = os.path.dirname(full_path)
            filename = os.path.basename(full_path)
            tasks.append((url, path, filename, artifact.get("sha1")))
        else:
            classifiers = downloads.get("classifiers", {})
            for cls_info in classifiers.values():
                url = normalize_url(cls_info.get("url"))
                full_path = os.path.join(base_path, "libraries", cls_info.get("path").replace("/", os.sep))
                path = os.path.dirname(full_path)
                filename = os.path.basename(full_path)
                tasks.append((url, path, filename, cls_info.get("sha1")))

    if not tasks:
        print("All dependencies are already present.")
        return

    print(f"Found {len(tasks)} files to verify or download.")
    progress_data = {'completed': 0, 'total': len(tasks)}
    progress_lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_download_worker, url, path, filename, progress_lock, progress_data, retries, timeout, expected_sha1)
            for url, path, filename, expected_sha1 in tasks
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass

    print("\nDependency download finished.")

def download_minecraft_client(version, path, show_progress=True):
    url = f"{BMCLAPI_BASE}/version/{version}/client"
    return download(url, path, f"{version}.jar", show_progress)

def download_minecraft_server(version, path, show_progress=True):
    url = f"{BMCLAPI_BASE}/version/{version}/server"
    return download(url, path, f"minecraft_server.{version}.jar", show_progress)

def download_version_json(version, path, show_progress=True):
    url = f"{BMCLAPI_BASE}/version/{version}/json"
    return download(url, path, f"{version}.json", show_progress)

def download_asset_object(hash_val, path, show_progress=True):
    hash_prefix = hash_val[:2]
    url = f"{BMCLAPI_BASE}/assets/{hash_prefix}/{hash_val}"
    return download(url, path, hash_val, show_progress, expected_sha1=hash_val)

def download_asset_index_file(asset_index_id, path, show_progress=True):
    url = f"{BMCLAPI_BASE}/assets/indexes/{asset_index_id}.json"
    return download(url, path, f"{asset_index_id}.json", show_progress)
    
def download_assets(asset_type, path, **kwargs):
    if asset_type == "client":
        return download_minecraft_client(kwargs["version"], path)
    elif asset_type == "server":
        return download_minecraft_server(kwargs["version"], path)
    elif asset_type == "assets_index":
        return download_version_json(kwargs["version"], path)
    elif asset_type == "asset_object":
        return download_asset_object(kwargs["hash"], path)
    elif asset_type == "url":
        return download(kwargs["url"], path, kwargs.get("filename"))
    else:
        raise ValueError(f"Unsupported asset type: {asset_type}")

def normalize_url(url: str) -> str:
    if not url:
        return url
    return url.replace("https://launchermeta.mojang.com/", f"{BMCLAPI_BASE}/") \
              .replace("https://launcher.mojang.com/", f"{BMCLAPI_BASE}/") \
              .replace("https://resources.download.minecraft.net/", f"{BMCLAPI_BASE}/assets/") \
              .replace("https://libraries.minecraft.net/", f"{BMCLAPI_BASE}/maven/")
