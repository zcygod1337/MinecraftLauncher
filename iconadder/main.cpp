#include<bits/stdc++.h>
#include<windows.h>
using namespace std;
double slowed=30;
void slow_print(string s) {
	for(int i=0; i<s.length(); i++) {
		cout << s[i];
		Sleep(slowed);
	}
	puts("");
}
bool file(string name) {
	ifstream file(name.c_str());
	return !file.fail();
}//查看文件是否存在 
void ero(){
	slow_print("dev by ");
	cout << "\n\n\n\n" << endl;
	cout << "\t                                                            .o8"<< endl;
	cout << "\t                                                           \"888" << endl;
	cout << "\t  oooooooo  .ooooo.  oooo    ooo  .oooooooo  .ooooo.   .oooo888" << endl;
	cout << "\t d'\"\"7d8P  d88' `\"Y8  `88.  .8'  888' `88b  d88' `88b d88' `888" << endl;
	cout << "\t   .d8P'   888         `88..8'   888   888  888   888 888   888" << endl;
	cout << "\t d8888888P  `Y8bod8P'     .8'     `8oooooo.  `Y8bod8P' `Y8bod88 \"" << endl;
	cout << "\t                     .o..P'      d\"     YD                     " << endl;
	cout << "\t                     `Y8P'       \"Y88888P'                     \n\n" << endl;
	slow_print("\n\n"); 
	system("color 03");
	Sleep(2000);
	system("cls");
	system("color 07");
}
int main(){
	ero();
	cout << "Minecraft Launcher,version 1.0.0,minecraft version 1.12.2" << endl;
	cout << "dev by zcygod" << endl;
	start:
	if(file("username.txt")){
		cout << "检测到您已设置用户名，是否启动？(请输入(1)启动,(2)重设用户名)" << endl;
		ifstream in("username.txt");
		string username;
		in>>username;
		int choose;
		cin >> choose;
		if(choose==1){
			string command = 
    ".\\jre\\bin\\java.exe "  // 使用与官方兼容的Java路径（或直接用官方Java路径）
    "-Dlog4j2.formatMsgNoLookups=true "
    "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump "
    "-Xmn399m "  // 官方指定的新生代内存
    "-Xmx2662m "  // 官方指定的最大内存
    "-Djava.library.path=\".\\.minecraft\\versions\\1.12.2\\1.12.2-natives\" "  // 原生库路径
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
    ".\\.minecraft\\libraries\\com\\mojang\\text2speech\\1.10.3\\text2speech-1.10.3.jar;"
    ".\\.minecraft\\versions\\1.12.2\\1.12.2.jar;" 
    "\" "
    "-Doolloo.jlw.tmpdir=\".\\test\" " 
    "-jar \".\\test\\JavaWrapper.jar\" " 
    "net.minecraft.client.main.Main "
    "--username " + username + " "  
    "--version 1.12.2 "
    "--gameDir \".\\.minecraft\\versions\\1.12.2\" "
    "--assetsDir \".\\.minecraft\\assets\" "
    "--assetIndex 1.12 "
    "--uuid 00000FFFFFFFFFFFFFFFFFFFFFF6B6BB "  
    "--accessToken 00000FFFFFFFFFFFFFFFFFFFFFF6B6BB "  
    "--userType msa "
    "--versionType zcy "
    "--height 480 " 
    "--width 854"; 
        	cout << "debug:" << command << endl;
			system(command.c_str());
		}else{
			in.close();
			system("del .\\username.txt");
			goto start;
			
		}
		
	}else {
		cout << "请先设置用户名!" << endl;
		ofstream out("username.txt");
		cout << "请问您的用户名是？（不可中文）" <<endl;
		string username;
		cin >> username;
		out << username;
		out.close();
		cout << "设置成功！" <<endl;
		goto start;
	}
	return 0;
}
