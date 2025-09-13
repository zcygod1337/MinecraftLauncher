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
        ofstream out("version.txt",ios::app);
        out << endl << version;
        out.close();
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
/*                                                            .o8  
                                                           "888  
  oooooooo  .ooooo.  oooo    ooo  .oooooooo  .ooooo.   .oooo888  
 d'""7d8P  d88' `"Y8  `88.  .8'  888' `88b  d88' `88b d88' `888  
   .d8P'   888         `88..8'   888   888  888   888 888   888  
 .d8P'  .P 888   .o8    `888'    `88bod8P'  888   888 888   888  
d8888888P  `Y8bod8P'     .8'     `8oooooo.  `Y8bod8P' `Y8bod88P" 
                     .o..P'      d"     YD                       
                     `Y8P'       "Y88888P'                       
                                                                 
																 
																 
*/

