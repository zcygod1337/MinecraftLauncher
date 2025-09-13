#include<bits/stdc++.h>
#include<windows.h>
#include "lib\run.hpp"
#include "lib\download.hpp" 
using namespace std;
string emptys;

/*


                                                            .o8  
                                                           "888  
  oooooooo  .ooooo.  oooo    ooo  .oooooooo  .ooooo.   .oooo888  
 d'""7d8P  d88' `"Y8  `88.  .8'  888' `88b  d88' `88b d88' `888  
   .d8P'   888         `88..8'   888   888  888   888 888   888  
 .d8P'  .P 888   .o8    `888'    `88bod8P'  888   888 888   888  
d8888888P  `Y8bod8P'     .8'     `8oooooo.  `Y8bod8P' `Y8bod88P" 
                     .o..P'      d"     YD                       
                     `Y8P'       "Y88888P'                       
                                                                 
                                                                 
*/
void help(){
	cout <<endl <<"使用帮助\n -run [version] --username [username]   以username为用户名，启动[version]版本的mc，如果没有找到该版本mc,会在当前目录下生成名字为\"not_found\"的文件"
	<< "-download [version] 下载[version]版本,后面忘了。(如果同时有多个任务，默认执行最后一个任务1)";
}
string task;
int main(int argc,char *argv[]){/*--MinecraftLauncher by zcygod version 1.0.2,添加命令行支持*/
	emptys.clear();
	if(argc==1){
		help();
	}
	if(argv[1]+emptys=="-help"){
		help();
	}
	string username="zcygod",version;
	for(int i=2;i<argc;i++){
		if(argv[i]=="-run"){
			task="run";
			version=argv[i+1];
		}
		if(argv[i]=="--username"){
			username=argv[i+1];
		}
		if(argv[i]=="-download"){
			task="download"; 
			version=argv[i+1];
		} 
	}
	if(task=="run"){
		bool flag=false;
		ifstream in("version.txt");
		string temp;
		while(in>>temp){
			if(temp==version){
				flag=true;
			}
		}
		if(!flag){
			cout << "没有你要启动的版本" << endl; 
			
		}
		minecraft::version=version;
		minecraft::username=username;
		minecraft::java_path=".\\jre\\bin\\java.exe";
	}else if(task=="download"){
		download::download_version(version);
		;;//cpp默认不支持文件库，故使用python实现了一个silent_downloader,简单调用 
	}
	while(1);
}
