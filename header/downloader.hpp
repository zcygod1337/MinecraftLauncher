#ifndef _DOWNLOAD_hpp
#define _DOWNLOAD_hpp
#include <bits/stdc++.h>
//QWQ
namespace download{

    inline bool file(const std::string& name) {
        std::ifstream fin(name.c_str()); 
        return !fin.fail();
    }
    std::string version;
    void download_version(std::string version){
        std::string command="downloader.exe "+version;
        system(command.c_str());
        // std::ofstream out("version.txt",ios::app);
        // std::out << std::endl << version;
        // out.close();
    }
    void download_java(){
        
        if(!file("java_good")){
            std::cout << "未检测到java环境，正在下载" << std::endl;
            system(".\\silent_downloader.exe -url https://github.com/zcygod1337/download/releases/download/JAVA_8/jre.7z");
            system(".\\7z.exe x jre.7z");
            if(!file("java_good")){
                std::cout << "你的网络爆炸了，请飞往国外下载" << std::endl; 
                while (1);
            }
        
        }
    }
};

#endif
