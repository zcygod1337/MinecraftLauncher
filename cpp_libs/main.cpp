#include<bits/stdc++.h>
void launch_minecraft(const std::string& version, const std::string& username) {
    // 获取必要路径
    std::string java_path = ".\\jre\\bin\\java.exe";
    std::string mc_dir = ".\\.minecraft";
    std::string natives_dir = mc_dir + "\\versions\\" + version + "\\natives";
    std::string client_jar = mc_dir + "\\versions\\" + version + "\\" + version + ".jar";

    // 构建启动命令
    std::string command = 
        "\"" + java_path + "\"" +
        " -Xms2G -Xmx4G" +
        " -Djava.library.path=\"" + natives_dir + "\"" +
        " -cp \"" + mc_dir + "\\libraries\\*;" + client_jar + "\"" +
        " net.minecraft.client.main.Main" +
        " --version " + version +
        " --assetIndex " + version +
        " --assetsDir \"" + mc_dir + "\\assets\"" +
        " --gameDir \"" + mc_dir + "\"" +
        " --username " + username +
        " --accessToken 0" +
        " --userType legacy";

    std::cout << "\n正在启动 Minecraft " << version << " ...\n" << std::endl;
    std::system(command.c_str());
}

int main(int argc, char* argv[]) {
    std::string version, username;

    // 通过命令行参数获取版本和用户名
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

    // 启动游戏
    launch_minecraft(version, username);

    return 0;
}

