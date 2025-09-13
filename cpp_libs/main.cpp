#include<bits/stdc++.h>
#include <fstream>
#include <windows.h>

// 检查文件是否存在（辅助函数，用于启动前校验）
bool file_exists(const std::string& path) {
    std::ifstream f(path.c_str());
    return f.good();
}

// 检查目录是否存在（辅助函数，用于启动前校验）
bool directory_exists(const std::string& path) {
    DWORD attr = GetFileAttributesA(path.c_str());
    return (attr != INVALID_FILE_ATTRIBUTES) && (attr & FILE_ATTRIBUTE_DIRECTORY);
}

// 构建动态版本的 Minecraft 启动命令（核心修改：用 version 参数替换所有 1.12.2 硬编码）
std::string buildLaunchCommand(const std::string& version, const std::string& username) {
    // 动态生成版本相关路径（根据传入的 version 参数）
    std::string natives_dir = ".\\.minecraft\\versions\\" + version + "\\" + "natives";
    std::string client_jar = ".\\.minecraft\\versions\\" + version + "\\" + version + ".jar";
    std::string game_dir = ".\\.minecraft\\versions\\" + version;

    // 拼接启动命令（所有版本相关内容均使用动态变量）
    std::string command = 
        ".\\jre\\bin\\java.exe "  // Java 可执行文件路径
        "-Dlog4j2.formatMsgNoLookups=true "  // 关闭 log4j2 安全漏洞
        "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump "  // 堆转储路径
        "-Xmn399m "  // 新生代内存大小（可根据需求调整）
        "-Xmx2662m "  // 最大堆内存大小（可根据需求调整）
        // 动态原生库路径（对应版本的 natives 目录）
        "-Djava.library.path=\"" + natives_dir + "\" "
        "-cp "  // 类路径开始
        "\""  // 类路径引号（处理路径中的空格）
        // 固定依赖库（Minecraft 通用依赖，不同版本基本一致，若版本差异大需调整）
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
        // 动态核心 JAR（对应传入的版本）
        client_jar + ";"
        "\" "  // 类路径引号结束
        // Minecraft 主类（固定，不同版本通用）
        "net.minecraft.client.main.Main "
        // 动态启动参数（所有版本相关配置均使用传入的 version）
        "--username " + username + " "  // 用户名（动态传入）
        "--version " + version + " "  // 游戏版本（动态传入）
        "--gameDir \"" + game_dir + "\" "  // 游戏目录（对应版本的目录）
        "--assetsDir \".\\.minecraft\\assets\" "  // 资源文件目录（固定，所有版本共享）
        "--assetIndex " + version + " "  // 资源索引版本（默认与游戏版本一致，可根据实际调整）
        "--uuid 00000FFFFFFFFFFFFFFFFFFFFFF6B6BB "  // 用户 UUID（固定，测试用；正式用需动态获取）
        "--accessToken 00000FFFFFFFFFFFFFFFFFFFFFF6B6BB "  // 访问令牌（固定，测试用；正式用需动态获取）
        "--userType msa "  // 用户类型（微软账号，固定）
        "--versionType zcy "  // 版本类型（自定义标识，固定）
        "--height 480 "  // 窗口高度（固定，可根据需求调整）
        "--width 854";  // 窗口宽度（固定，可根据需求调整）

    return command;
}

// 启动 Minecraft 核心函数（增加版本文件校验）
void launch_minecraft(const std::string& version, const std::string& username) {
    // 先校验版本相关文件是否存在，避免启动失败
    std::string natives_dir = ".\\.minecraft\\versions\\" + version + "\\" + version + "-natives";
    std::string client_jar = ".\\.minecraft\\versions\\" + version + "\\" + version + ".jar";
    std::string game_dir = ".\\.minecraft\\versions\\" + version;

    // 校验 Java 路径
    if (!file_exists(".\\jre\\bin\\java.exe")) {
        std::cerr << "错误: 找不到 Java 可执行文件 .\\jre\\bin\\java.exe" << std::endl;
        return;
    }

    // 校验游戏版本目录
    if (!directory_exists(game_dir)) {
        std::cerr << "错误: 找不到版本 " << version << " 的目录 " << game_dir << std::endl;
        std::cerr << "请确保该版本已正确安装（目录结构：.minecraft/versions/[版本号]/）" << std::endl;
        return;
    }

    // 校验核心 JAR 文件
    if (!file_exists(client_jar)) {
        std::cerr << "错误: 找不到版本 " << version << " 的核心文件 " << client_jar << std::endl;
        return;
    }

    // 校验原生库目录（部分版本可能无此目录，可注释此校验）
    if (!directory_exists(natives_dir)) {
        std::cerr << "警告: 找不到版本 " << version << " 的原生库目录 " << natives_dir << std::endl;
        std::cerr << "部分功能可能无法正常使用，建议检查版本安装完整性" << std::endl;
    }

    // 构建并执行启动命令
    std::string command = buildLaunchCommand(version, username);
    std::cout << "\n正在启动 Minecraft " << version << " ...\n" << std::endl;
    std::cout << "启动命令: " << command << std::endl;  // 输出命令用于调试

    int result = std::system(command.c_str());
    
    // 输出启动结果
    std::cout << "\n--------------------------------" << std::endl;
    std::cout << "Process exited with return value " << result << std::endl;
}

// 主函数（保持原交互逻辑）
int main(int argc, char* argv[]) {
    std::string version, username;

    // 优先通过命令行参数获取版本和用户名（格式：启动器.exe [版本号] [用户名]）
    if (argc == 3) {
        version = argv[1];
        username = argv[2];
    } else {
        // 命令行参数不足时，手动输入
        std::cout << "Minecraft 启动器" << std::endl;
        std::cout << "请输入版本号: ";
        std::getline(std::cin, version);
        std::cout << "请输入用户名: ";
        std::getline(std::cin, username);
    }

    // 启动游戏（传入动态版本和用户名）
    launch_minecraft(version, username);

    std::cout << "请按任意键继续. . .";
    std::cin.get();  // 等待用户按键，避免窗口直接关闭
    return 0;
}
