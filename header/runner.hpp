#ifndef _RUNNER_hpp
#define _RUNNER_hpp
#include <bits/stdc++.h>
#include <fstream>
using namespace std;
//爆炸后因为我不会写库于是狂暴请教豆包 
namespace launcher {
    std::string username = "zcygod";
    std::string version;  // 版本将在启动时动态设置
    std::string natives_dir;
    std::string client_jar;
    std::string game_dir;
    std::string assets_dir = ".\\.minecraft\\assets";
    std::string asset_index;
    std::string command;
    
    // 获取所有版本通用的核心库列表（手动维护）
    vector<string> get_core_libraries() {
        return {
            // 基础依赖库
            ".\\.minecraft\\libraries\\com\\mojang\\patchy\\1.3.9\\patchy-1.3.9.jar",
            ".\\.minecraft\\libraries\\oshi-project\\oshi-core\\1.1\\oshi-core-1.1.jar",
            ".\\.minecraft\\libraries\\net\\java\\dev\\jna\\jna\\4.4.0\\jna-4.4.0.jar",
            ".\\.minecraft\\libraries\\net\\java\\dev\\jna\\platform\\3.4.0\\platform-3.4.0.jar",
            ".\\.minecraft\\libraries\\com\\ibm\\icu\\icu4j-core-mojang\\51.2\\icu4j-core-mojang-51.2.jar",
            
            ".\\.minecraft\\libraries\\net\\sf\\jopt-simple\\jopt-simple\\5.0.3\\jopt-simple-5.0.3.jar",
            ".\\.minecraft\\libraries\\net\\sf\\jopt-simple\\jopt-simple\\4.6\\jopt-simple-4.6.jar",
            
            // 音频库
            ".\\.minecraft\\libraries\\com\\paulscode\\codecjorbis\\20101023\\codecjorbis-20101023.jar",
            ".\\.minecraft\\libraries\\com\\paulscode\\codecwav\\20101023\\codecwav-20101023.jar",
            ".\\.minecraft\\libraries\\com\\paulscode\\libraryjavasound\\20101123\\libraryjavasound-20101123.jar",
            ".\\.minecraft\\libraries\\com\\paulscode\\librarylwjglopenal\\20100824\\librarylwjglopenal-20100824.jar",
            ".\\.minecraft\\libraries\\com\\paulscode\\soundsystem\\20120107\\soundsystem-20120107.jar",
            
            // 网络库
            ".\\.minecraft\\libraries\\io\\netty\\netty-all\\4.1.9.Final\\netty-all-4.1.9.Final.jar",
            ".\\.minecraft\\libraries\\io\\netty\\netty-all\\4.0.23.Final\\netty-all-4.0.23.Final.jar",
            
            // 工具库
            ".\\.minecraft\\libraries\\com\\google\\guava\\guava\\21.0\\guava-21.0.jar",
            ".\\.minecraft\\libraries\\com\\google\\guava\\guava\\17.0\\guava-17.0.jar",
            ".\\.minecraft\\libraries\\org\\apache\\commons\\commons-lang3\\3.5\\commons-lang3-3.5.jar",
            ".\\.minecraft\\libraries\\org\\apache\\commons\\commons-lang3\\3.3.2\\commons-lang3-3.3.2.jar",
            ".\\.minecraft\\libraries\\commons-io\\commons-io\\2.5\\commons-io-2.5.jar",
            ".\\.minecraft\\libraries\\commons-io\\commons-io\\2.4\\commons-io-2.4.jar",
            ".\\.minecraft\\libraries\\commons-codec\\commons-codec\\1.10\\commons-codec-1.10.jar",
            ".\\.minecraft\\libraries\\commons-codec\\commons-codec\\1.9\\commons-codec-1.9.jar",
            
            // 输入输出库
            ".\\.minecraft\\libraries\\net\\java\\jinput\\jinput\\2.0.5\\jinput-2.0.5.jar",
            ".\\.minecraft\\libraries\\net\\java\\jutils\\jutils\\1.0.0\\jutils-1.0.0.jar",
            
            // JSON处理库
            ".\\.minecraft\\libraries\\com\\google\\code\\gson\\gson\\2.8.0\\gson-2.8.0.jar",
            ".\\.minecraft\\libraries\\com\\google\\code\\gson\\gson\\2.2.4\\gson-2.2.4.jar",
            
            // 认证库
            ".\\.minecraft\\libraries\\com\\mojang\\authlib\\1.5.25\\authlib-1.5.25.jar",
            ".\\.minecraft\\libraries\\com\\mojang\\authlib\\1.5.21\\authlib-1.5.21.jar",
            
            //  realms库
            ".\\.minecraft\\libraries\\com\\mojang\\realms\\1.10.22\\realms-1.10.22.jar",
            ".\\.minecraft\\libraries\\com\\mojang\\realms\\1.7.59\\realms-1.7.59.jar",
            
            // 压缩库
            ".\\.minecraft\\libraries\\org\\apache\\commons\\commons-compress\\1.8.1\\commons-compress-1.8.1.jar",
            
            // HTTP库
            ".\\.minecraft\\libraries\\org\\apache\\httpcomponents\\httpclient\\4.3.3\\httpclient-4.3.3.jar",
            ".\\.minecraft\\libraries\\commons-logging\\commons-logging\\1.1.3\\commons-logging-1.1.3.jar",
            ".\\.minecraft\\libraries\\org\\apache\\httpcomponents\\httpcore\\4.3.2\\httpcore-4.3.2.jar",
            
            // 日志库
            ".\\.minecraft\\libraries\\org\\apache\\logging\\log4j\\log4j-api\\2.8.1\\log4j-api-2.8.1.jar",
            ".\\.minecraft\\libraries\\org\\apache\\logging\\log4j\\log4j-core\\2.8.1\\log4j-core-2.8.1.jar",
            ".\\.minecraft\\libraries\\org\\apache\\logging\\log4j\\log4j-api\\2.0-beta9\\log4j-api-2.0-beta9.jar",
            ".\\.minecraft\\libraries\\org\\apache\\logging\\log4j\\log4j-core\\2.0-beta9\\log4j-core-2.0-beta9.jar",
            
            // LWJGL库（不同版本兼容）
            ".\\.minecraft\\libraries\\org\\lwjgl\\lwjgl\\lwjgl\\2.9.4-nightly-20150209\\lwjgl-2.9.4-nightly-20150209.jar",
            ".\\.minecraft\\libraries\\org\\lwjgl\\lwjgl\\lwjgl_util\\2.9.4-nightly-20150209\\lwjgl_util-2.9.4-nightly-20150209.jar",
            ".\\.minecraft\\libraries\\org\\lwjgl\\lwjgl\\lwjgl\\2.9.2-nightly-20140822\\lwjgl-2.9.2-nightly-20140822.jar",
            ".\\.minecraft\\libraries\\org\\lwjgl\\lwjgl\\lwjgl_util\\2.9.2-nightly-20140822\\lwjgl_util-2.9.2-nightly-20140822.jar",
            
            // 其他必要库
            ".\\.minecraft\\libraries\\com\\mojang\\text2speech\\1.10.3\\text2speech-1.10.3.jar",
            ".\\.minecraft\\libraries\\it\\unimi\\dsi\\fastutil\\7.1.0\\fastutil-7.1.0.jar"
        };
    }
    
    // 加载资源索引信息（从版本文件获取正确的assetIndex）
    void load_asset_index(const string& version_id) {
        string path = ".\\.minecraft\\versions\\" + version_id + "\\" + version_id + ".json";
        ifstream file(path);
        
        if (!file.is_open()) {
            cerr << "无法打开版本文件: " << path << endl;
            return;
        }
        
        string content((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
        file.close();
        
        // 提取资源索引
        size_t pos = content.find("\"assetIndex\"");
        if (pos != string::npos) {
            pos = content.find("\"id\":", pos) + 5;
            pos = content.find("\"", pos) + 1;
            size_t end = content.find("\"", pos);
            asset_index = content.substr(pos, end - pos);
        }
    }
    
    // 设置版本并更新路径
    void set_version(const string& ver) {
        version = ver;
        natives_dir = ".\\.minecraft\\versions\\" + version + "\\natives";
        client_jar = ".\\.minecraft\\versions\\" + version + "\\" + version + ".jar";
        game_dir = ".\\.minecraft";
        
        // 加载资源索引
        load_asset_index(version);
    }
    
    // 构建启动命令（使用手动维护的核心库列表）
    void build_command() {
        // 获取核心库列表
        vector<string> libraries = get_core_libraries();
        string classpath;
        for (const string& lib : libraries) {
            // 检查库文件是否存在，存在才添加到类路径
            if (ifstream(lib)) {
                if (!classpath.empty()) {
                    classpath += ";";
                }
                classpath += "\"" + lib + "\"";
            }
        }
        
        if (!classpath.empty()) {
            classpath += ";";
        }
        classpath += "\"" + client_jar + "\"";
        
        // 构建完整命令
        command = 
            ".\\jre\\bin\\java.exe " 
            "-Dlog4j2.formatMsgNoLookups=true " 
            "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump " 
            "-Xmn399m "  
            "-Xmx2662m "  
            "-Djava.library.path=\"" + natives_dir + "\" "
            "-cp " + classpath + " "
            "net.minecraft.client.main.Main "
            "--username " + username + " " 
            "--version " + version + " "  
            "--gameDir \"" + game_dir + "\" "  
            "--assetsDir \"" + assets_dir + "\" "  
            "--assetIndex " + asset_index + " "  
            "--uuid 0 "  
            "--accessToken 0 "
            "--userType msa " 
            "--versionType release "  
            "--height 480 " 
            "--width 854";
    }
    
    // 启动指定版本
    void launch(const string& ver) {
        set_version(ver);
        build_command();
        
        // 输出命令用于调试
        cout << "启动命令: " << command << endl;
        
        // 执行命令
        system(command.c_str());
    }
    
    // 保留原有launch方法的兼容性
    void launch() {
        if (!version.empty()) {
            build_command();
            system(command.c_str());
        } else {
            cerr << "请先设置版本号" << endl;
        }
    }
};
#endif
    
