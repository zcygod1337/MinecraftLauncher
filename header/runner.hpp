#ifndef _RUNNER_hpp
#define _RUNNER_hpp
#include <bits/stdc++.h>
using namespace std;

namespace launcher{
    std::string username="zcygod";
    std::string version;
    std::string natives_dir = ".\\.minecraft\\versions\\" + version + "\\" + "natives";
    std::string client_jar = ".\\.minecraft\\versions\\" + version + "\\" + version + ".jar";
    std::string game_dir = ".\\.minecraft\\versions\\" + version;
    std::string command = 
        ".\\jre\\bin\\java.exe " 
        "-Dlog4j2.formatMsgNoLookups=true " 
        "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump " 
        "-Xmn399m "  
        "-Xmx2662m "  
        "-Djava.library.path=\"" + natives_dir + "\" "
        "-cp " 
        "\""  
        ".\\.minecraft\\libraries\\com\\mojang\\patchy\\1.3.9\\patchy-1.3.9.jar;"
        ".\\.minecraft\\libraries\\oshi-project\\oshi-core\\1.1\\oshi-core-1.1.jar;"
        ".\\.minecraft\\libraries\\net\\java\\dev\\jna\\jna\\4.4.0\\jna-4.4.0.jar;"
        ".\\.minecraft\\libraries\\net\\java\\dev\\jna\\platform\\3.4.0\\platform-3.4.0.jar;"
        ".\\.minecraft\\libraries\\com\\ibm\\icu\\icu4j-core-mojang\\51.2\\icu4j-core-mojang-51.2.jar;"
        ".\\.minecraft\\libraries\\net\\sf\\jopt-simple\\jopt-simple\\5.0.3\\jopt-simple-5.0.3.jar;"
        ".\\.minecraft\\libraries\\com\\paulscode\\codecjorbis\\20101023\\codecjorbis-20101023.jar;"
        ".\\.minecraft\\libraries\\com\\paulscode\\codecwav\\20101023\\codecwav-20101023.jar;"
        ".\\.minecraft\\libraries\\com\\paulscode\\libraryjavasound\\20101123\\libraryjavasound-20101123.jar;"
        ".\\.minecraft\\libraries\\com\\paulscode\\librarylwjglopenal\\20100824\\librarylwjglopenal-20100824.jar;"
        ".\\.minecraft\\libraries\\com\\paulscode\\soundsystem\\20120107\\soundsystem-20120107.jar;"
        ".\\.minecraft\\libraries\\io\\netty\\netty-all\\4.1.9.Final\\netty-all-4.1.9.Final.jar;"
        ".\\.minecraft\\libraries\\com\\google\\guava\\guava\\21.0\\guava-21.0.jar;"
        ".\\.minecraft\\libraries\\org\\apache\\commons\\commons-lang3\\3.5\\commons-lang3-3.5.jar;"
        ".\\.minecraft\\libraries\\commons-io\\commons-io\\2.5\\commons-io-2.5.jar;"
        ".\\.minecraft\\libraries\\commons-codec\\commons-codec\\1.10\\commons-codec-1.10.jar;"
        ".\\.minecraft\\libraries\\net\\java\\jinput\\jinput\\2.0.5\\jinput-2.0.5.jar;"
        ".\\.minecraft\\libraries\\net\\java\\jutils\\jutils\\1.0.0\\jutils-1.0.0.jar;"
        ".\\.minecraft\\libraries\\com\\google\\code\\gson\\gson\\2.8.0\\gson-2.8.0.jar;"
        ".\\.minecraft\\libraries\\com\\mojang\\authlib\\1.5.25\\authlib-1.5.25.jar;"
        ".\\.minecraft\\libraries\\com\\mojang\\realms\\1.10.22\\realms-1.10.22.jar;"
        ".\\.minecraft\\libraries\\org\\apache\\commons\\commons-compress\\1.8.1\\commons-compress-1.8.1.jar;"
        ".\\.minecraft\\libraries\\org\\apache\\httpcomponents\\httpclient\\4.3.3\\httpclient-4.3.3.jar;"
        ".\\.minecraft\\libraries\\commons-logging\\commons-logging\\1.1.3\\commons-logging-1.1.3.jar;"
        ".\\.minecraft\\libraries\\org\\apache\\httpcomponents\\httpcore\\4.3.2\\httpcore-4.3.2.jar;"
        ".\\.minecraft\\libraries\\it\\unimi\\dsi\\fastutil\\7.1.0\\fastutil-7.1.0.jar;"
        ".\\.minecraft\\libraries\\org\\apache\\logging\\log4j\\log4j-api\\2.8.1\\log4j-api-2.8.1.jar;"
        ".\\.minecraft\\libraries\\org\\apache\\logging\\log4j\\log4j-core\\2.8.1\\log4j-core-2.8.1.jar;"
        ".\\.minecraft\\libraries\\org\\lwjgl\\lwjgl\\lwjgl\\2.9.4-nightly-20150209\\lwjgl-2.9.4-nightly-20150209.jar;"
        ".\\.minecraft\\libraries\\org\\lwjgl\\lwjgl\\lwjgl_util\\2.9.4-nightly-20150209\\lwjgl_util-2.9.4-nightly-20150209.jar;"
        ".\\.minecraft\\libraries\\com\\mojang\\text2speech\\1.10.3\\text2speech-1.10.3.jar;"+

        client_jar + ";"
        "\" "  
        
        "net.minecraft.client.main.Main "
        "--username " + username + " " 
        "--version " + version + " "  
        "--gameDir \"" + game_dir + "\" "  
        "--assetsDir \".\\.minecraft\\assets\" "  
        "--assetIndex " + version + " "  
        "--uuid 0 "  
        "--accessToken 0"
        "--userType msa " 
        "--versionType zcy "  
        "--height 480 " 
        "--width 854"; 
        void launch(){
            system(command.c_str());
            // string temp;
            // ifstream in("version.txt");
            // bool flag=false;
            // while(in>> temp){
            //     if(temp==version){
            //         system(command.c_str());
            //         flag=true;
            //         break;
            //     }
            // }
            // if(!flag){
            //     cout << "错误：未检测到版本 "+version+"，请先下载该版本"<<endl;
            //     cout << "按任意键退出"<<endl;
            //     while(1);
            // }
            // in.close();
        }
};
#endif
//2025/9/14 14:21 补：这个命令行指令是从PCL抄来的，但是暂时因为包含库原因不能用
