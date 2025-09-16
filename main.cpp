#include<bits/stdc++.h>
#include<windows.h>
#include"./header/downloader.hpp"
#include"./header/runner.hpp"


using namespace std;
string empty;
void help(){
    cout << "========================================================="<<endl;
    cout << "Minecraft Launcher by C++"<<endl;  
    cout << "          --dev by zcygod" << endl;
    cout << "1. ./{filename} -run {version} --username {name} 以{username}运行{version}版本的minecraft"<<endl;
    cout << "2. ./{filename} -download {version} 下载{version}版本的Minecraft及支持库"<<endl;
    // cout << "3. ./{filename} -download_jdk8 下载java8（默认第一次运行会执行）"<<endl;
    cout << "3. ./{filename} -help 获取帮助"<<endl;
    cout << "========================================================="<<endl;
}
int main(int argc,char* argv[]){
    download::download_java();
    empty.clear();
    if(argv[1]=="-help"){
        test:
        help();
        while(1);
    }
    if(argc<=1){
        cout<< endl << "检测到 您没有设置参数，自动跳转到-help"<<endl;
        goto test;
    }
    for(int i=1;i<argc;i++){
        if((string)argv[i]=="-download"){
            cout << "debug:download" << endl;
            if(i+1<argc){
                download::download_version(argv[i+1]);
                cout << "下载完成，按任意键退出"<<endl;
                while(1);
            }else{
                cout << "错误：-download 后缺少版本号"<<endl;
                cout << "按任意键退出"<<endl;
                while(1);
            }
        }
        if((string)argv[i]=="-download_jdk8"){
            download::download_java();
            cout << "下载完成，按任意键退出"<<endl;
            while(1);
        }
        if((string)argv[i]=="-run"){
            launcher::version=argv[i+1];
            launcher::username=argv[i+3];
            if(launcher::version>="1.16.5"){
            	launcher::set_java_path(".\\jre17\\bin\\java.exe");
			}
            // }else{
            //     cout << "错误：-run 后缺少 --username {name}"<<endl;
            //     cout << "按Ctrl+C"<<endl;
            //     while(1);  
            // }
            launcher::launch();
        }

    }
    cout << "end" <<endl;
    while(true);
}
