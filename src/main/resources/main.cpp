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
    cout << "1. ./{filename} -run {version} --username {name} ��{username}����{version}�汾��minecraft"<<endl;
    cout << "2. ./{filename} -download {version} ����{version}�汾��Minecraft��֧�ֿ�"<<endl;
    cout << "3. ./{filename} -download_jdk8 ����java8��Ĭ�ϵ�һ�����л�ִ�У�"<<endl;
    cout << "3. ./{filename} -help ��ȡ����"<<endl;
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
        cout<< endl << "��⵽ ��û�����ò������Զ���ת��-help"<<endl;
        goto test;
    }
    for(int i=1;i<argc;i++){
        if((string)argv[i]=="-download"){
            cout << "debug:download" << endl;
            if(i+1<argc){
                download::download_version(argv[i+1]);
                cout << "������ɣ���������˳�"<<endl;
                while(1);
            }else{
                cout << "����-download ��ȱ�ٰ汾��"<<endl;
                cout << "��������˳�"<<endl;
                while(1);
            }
        }
        if((string)argv[i]=="-download_jdk8"){
            download::download_java();
            cout << "������ɣ���������˳�"<<endl;
            while(1);
        }
        if((string)argv[i]=="-run"){
            launcher::version=argv[i+1];
            launcher::username=argv[i+3];
            // }else{
            //     cout << "����-run ��ȱ�� --username {name}"<<endl;
            //     cout << "��Ctrl+C"<<endl;
            //     while(1);  
            // }
            launcher::launch(launcher::version);
        }

    }
    cout << "end" <<endl;
    while(true);
}
