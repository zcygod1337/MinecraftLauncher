#ifndef _RUNNER_hpp
#define _RUNNER_hpp
#include <bits/stdc++.h>
#include <fstream>
#include <direct.h> // Windows目录操作
#include <io.h>     // Windows文件操作
#include "json.hpp" // 需要将nlohmann/json.hpp放在同一目录

using namespace std;
using json = nlohmann::json;

namespace launcher {
    std::string username = "zcygod";
    std::string version;  
    std::string natives_dir;
    std::string client_jar;
    std::string game_dir;
    std::string assets_dir = ".minecraft\\assets";
    std::string asset_index;
    std::string command;
    std::vector<std::string> libraries;
    
    // 检查文件或目录是否存在（Windows专用）
    bool path_exists(const string& path) {
        return _access(path.c_str(), 0) == 0;
    }
    
    // 创建目录（Windows专用）
    bool create_directory(const string& path) {
        return _mkdir(path.c_str()) == 0;
    }
    
    // 创建多级目录（Windows专用）
    bool create_directories(const string& path) {
        string current_path;
        size_t pos = 0;
        
        while ((pos = path.find('\\', pos + 1)) != string::npos) {
            current_path = path.substr(0, pos);
            if (!path_exists(current_path)) {
                if (!create_directory(current_path)) {
                    return false;
                }
            }
        }
        
        if (!path_exists(path)) {
            return create_directory(path);
        }
        return true;
    }
    
    // 获取文件名（不含路径）
    string get_filename(const string& path) {
        size_t pos = path.find_last_of("\\");
        if (pos != string::npos) {
            return path.substr(pos + 1);
        }
        return path;
    }
    
    // 版本比较函数
    bool is_version_at_least(const string& version, const string& target) {
        if (version.empty()) return false;
        
        vector<int> ver_parts, target_parts;
        stringstream ver_ss(version), target_ss(target);
        string part;
        
        while (getline(ver_ss, part, '.')) {
            try {
                ver_parts.push_back(stoi(part));
            } catch (...) {
                ver_parts.push_back(0);
            }
        }
        while (getline(target_ss, part, '.')) {
            try {
                target_parts.push_back(stoi(part));
            } catch (...) {
                target_parts.push_back(0);
            }
        }
        
        for (size_t i = 0; i < max(ver_parts.size(), target_parts.size()); i++) {
            int ver_num = (i < ver_parts.size()) ? ver_parts[i] : 0;
            int target_num = (i < target_parts.size()) ? target_parts[i] : 0;
            
            if (ver_num > target_num) return true;
            if (ver_num < target_num) return false;
        }
        return true;
    }
    
    // 获取Java路径
    string get_java_path() {
        if (!version.empty() && is_version_at_least(version, "1.17")) {
            // 检查jre17是否存在
            if (path_exists(".\\jre17\\bin\\java.exe")) {
                return ".\\jre17\\bin\\java.exe";
            }
        }
        
        // 默认使用jre8
        if (path_exists(".\\jre\\bin\\java.exe")) {
            return ".\\jre\\bin\\java.exe";
        }
        
        // 如果自定义JRE不存在，使用系统Java
        return "java.exe";
    }
    
    // 从version_info.json加载库文件信息
    bool load_libraries_from_json(const string& json_path = "version_info.json") {
        ifstream file(json_path);
        if (!file.is_open()) {
            cerr << "无法打开版本信息文件: " << json_path << endl;
            return false;
        }
        
        try {
            json j;
            file >> j;
            
            // 读取基本路径信息
            if (j.contains("minecraft_dir")) {
                game_dir = j["minecraft_dir"].get<string>();
            }
            if (j.contains("client_jar")) {
                client_jar = j["client_jar"].get<string>();
            }
            if (j.contains("natives_dir")) {
                natives_dir = j["natives_dir"].get<string>();
            }
            if (j.contains("assets_dir")) {
                assets_dir = j["assets_dir"].get<string>();
            }
            if (j.contains("asset_index")) {
                asset_index = j["asset_index"].get<string>();
            }
            if (j.contains("version_id")) {
                version = j["version_id"].get<string>();
            }
            
            // 读取库文件列表
            if (j.contains("libraries") && j["libraries"].is_array()) {
                libraries.clear();
                for (const auto& lib_path : j["libraries"]) {
                    libraries.push_back(lib_path.get<string>());
                }
                cout << "从JSON加载了 " << libraries.size() << " 个库文件" << endl;
            }
            
            return true;
        } catch (const exception& e) {
            cerr << "解析JSON文件失败: " << e.what() << endl;
            return false;
        }
    }
    
    // 检查文件是否存在
    bool file_exists(const string& path) {
        return path_exists(path);
    }
    
    vector<string> get_core_libraries() {
        vector<string> result_libraries;
        
        // 首先添加从JSON加载的库文件
        for (const string& lib : libraries) {
            if (file_exists(lib)) {
                result_libraries.push_back(lib);
                cout << "添加库: " << get_filename(lib) << endl;
            } else {
                cerr << "警告: 库文件不存在: " << lib << endl;
            }
        }
        
        // 对于1.13+版本，添加必要的LWJGL 3.x库（如果JSON中未包含）
        if (!version.empty() && is_version_at_least(version, "1.13")) {
            vector<string> modern_libs = {
                ".minecraft\\libraries\\org\\lwjgl\\lwjgl\\3.2.2\\lwjgl-3.2.2.jar",
                ".minecraft\\libraries\\org\\lwjgl\\lwjgl-glfw\\3.2.2\\lwjgl-glfw-3.2.2.jar",
                ".minecraft\\libraries\\org\\lwjgl\\lwjgl-jemalloc\\3.2.2\\lwjgl-jemalloc-3.2.2.jar",
                ".minecraft\\libraries\\org\\lwjgl\\lwjgl-openal\\3.2.2\\lwjgl-openal-3.2.2.jar",
                ".minecraft\\libraries\\org\\lwjgl\\lwjgl-opengl\\3.2.2\\lwjgl-opengl-3.2.2.jar",
                ".minecraft\\libraries\\org\\lwjgl\\lwjgl-stb\\3.2.2\\lwjgl-stb-3.2.2.jar",
                
                // 其他1.13+库
                ".minecraft\\libraries\\com\\mojang\\datafixerupper\\2.0.24\\datafixerupper-2.0.24.jar",
                ".minecraft\\libraries\\com\\mojang\\flatbuffers\\1.12.0\\flatbuffers-1.12.0.jar",
                ".minecraft\\libraries\\com\\mojang\\javabridge\\1.0.22\\javabridge-1.0.22.jar"
            };
            
            for (const string& lib : modern_libs) {
                if (file_exists(lib)) {
                    // 检查是否已经添加过
                    if (find(result_libraries.begin(), result_libraries.end(), lib) == result_libraries.end()) {
                        result_libraries.push_back(lib);
                        cout << "添加额外库: " << get_filename(lib) << endl;
                    }
                }
            }
        }
        
        // 添加客户端jar文件
        if (file_exists(client_jar)) {
            result_libraries.push_back(client_jar);
            cout << "添加客户端: " << get_filename(client_jar) << endl;
        } else {
            cerr << "错误: 客户端jar文件不存在: " << client_jar << endl;
        }
        
        return result_libraries;
    }
    
    void load_asset_index(const string& version_id) {
        string path = ".minecraft\\versions\\" + version_id + "\\" + version_id + ".json";
        ifstream file(path);
        
        if (!file.is_open()) {
            cerr << "无法打开版本文件: " << path << endl;
            return;
        }
        
        try {
            json j;
            file >> j;
            
            if (j.contains("assetIndex") && j["assetIndex"].is_object() && j["assetIndex"].contains("id")) {
                asset_index = j["assetIndex"]["id"].get<string>();
                cout << "资源索引: " << asset_index << endl;
            }
        } catch (const exception& e) {
            cerr << "解析版本JSON失败: " << e.what() << endl;
        }
    }
    
    // 将启动命令写入bat文件
    void write_to_bat_file(const string& cmd) {
        ofstream bat_file("Lastest_launch.bat");
        if (bat_file.is_open()) {
            bat_file << "@echo off\n";
            // bat_file << "chcp 65001 > nul\n";
            bat_file << "echo 正在启动 Minecraft " << version << "...\n";
            bat_file << "cd /D \"%~dp0\"\n";
            bat_file << cmd << "\n";
            bat_file << "if %errorlevel% neq 0 (\n";
            bat_file << "    echo 启动失败，错误代码: %errorlevel%\n";
            bat_file << "    echo 请检查Java环境和游戏文件是否完整\n";
            bat_file << ")\n";
            bat_file << "pause\n";
            bat_file.close();
            cout << "启动命令已写入 Lastest_launch.bat" << endl;
        } else {
            cerr << "无法创建 Lastest_launch.bat 文件" << endl;
        }
    }
    
    // 设置版本并更新路径
    void set_version(const string& ver) {
        version = ver;
        natives_dir = ".minecraft\\versions\\" + version + "\\natives";
        client_jar = ".minecraft\\versions\\" + version + "\\" + version + ".jar";
        game_dir = ".minecraft";
        
        // 加载资源索引
        load_asset_index(version);
    }
    
    void build_command() {
        // 首先尝试从JSON文件加载库文件信息
        if (!load_libraries_from_json()) {
            cerr << "使用默认库文件配置" << endl;
            // 如果JSON加载失败，使用默认设置
            set_version(version);
        }
        
        // 获取核心库列表
        vector<string> libraries_list = get_core_libraries();
        if (libraries_list.empty()) {
            cerr << "错误: 没有可用的库文件" << endl;
            return;
        }
        
        string classpath;
        cout << "构建类路径..." << endl;
        for (const string& lib : libraries_list) {
            if (file_exists(lib)) {
                if (!classpath.empty()) {
                    classpath += ";";
                }
                classpath += "\"" + lib + "\"";
            }
        }
        
        // 获取正确的Java路径
        string java_path = get_java_path();
        cout << "使用Java: " << java_path << endl;
        
        // 检查natives目录
        if (!path_exists(natives_dir)) {
            cerr << "警告: natives目录不存在: " << natives_dir << endl;
            if (!create_directories(natives_dir)) {
                cerr << "创建natives目录失败" << endl;
            }
        }
        
        // 构建完整命令 - 修复这里的字符串连接错误
        command = 
            "\"" + java_path + "\" " 
            "-Dlog4j2.formatMsgNoLookups=true " 
            "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump " 
            "-Xmx2G " 
            "-Djava.library.path=\"" + natives_dir + "\" "
            "-cp " + classpath + " "
            "net.minecraft.client.main.Main "
            "--username " + username + " " 
            "--version " + version + " "  // 这里修复了，使用 + 而不是 <<
            "--gameDir \"" + game_dir + "\" "  
            "--assetsDir \"" + assets_dir + "\" "  
            "--assetIndex " + asset_index + " "  
            "--uuid 00000000-0000-0000-0000-000000000000 "  
            "--accessToken 0 "
            "--userType msa " 
            "--versionType release "  
            "--width 854 "
            "--height 480";
            
        cout << "命令构建完成" << endl;
    }
    
    // 启动指定版本
    void launch(const string& ver) {
        cout << "=== 启动 Minecraft " << ver << " ===" << endl;
        set_version(ver);
        build_command();
        
        if (command.empty()) {
            cerr << "构建命令失败，请检查错误信息" << endl;
            return;
        }
        
        // 将启动命令写入bat文件
        write_to_bat_file(command);
        
        cout << "执行启动命令..." << endl;
        // 执行启动命令
        system("Lastest_launch.bat");
    }
    
    // 使用JSON文件中的信息启动
    void launch_from_json(const string& json_path = "version_info.json") {
        cout << "=== 从JSON文件启动 ===" << endl;
        if (load_libraries_from_json(json_path)) {
            build_command();
            
            if (command.empty()) {
                cerr << "构建命令失败，请检查错误信息" << endl;
                return;
            }
            
            // 将启动命令写入bat文件
            write_to_bat_file(command);
            
            cout << "执行启动命令..." << endl;
            // 执行启动命令
            int result = system(command.c_str());
            if (result != 0) {
                cerr << "启动失败，返回代码: " << result << endl;
                cerr << "请检查Java环境和游戏文件是否完整" << endl;
            }
        } else {
            cerr << "无法从JSON文件加载版本信息" << endl;
        }
    }
    
    void launch() {
        if (!version.empty()) {
            launch(version);
        } else {
            // 尝试从JSON自动检测版本
            launch_from_json();
        }
    }
};
#endif