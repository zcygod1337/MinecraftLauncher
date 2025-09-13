#ifndef _RUN_hpp
#define _RUN_hpp

#include <string>
#include <cstdlib>
namespace minecraft {
    std::string version;
    std::string username; 
    std::string java_path;
    std::string mc_dir=".\\.minecraft";
    void run_client() {
        std::string command = java_path + 
            " -Xms2G -Xmx4G" + 
            " -Djava.library.path=" + mc_dir + "\\versions\\" + version + "\\natives" +
            " -cp " + mc_dir + "\\libraries\\*;" + 
                     mc_dir + "\\versions\\" + version + "\\" + version + ".jar" +
            " net.minecraft.client.main.Main" +
            " --version " + version +
            " --assetIndex " + version +
            " --assetsDir " + mc_dir + "\\assets" +
            " --gameDir " + mc_dir +
            " --username " + username +
            " --accessToken 0" + 
            " --userType legacy";
        system(command.c_str());
    }
}

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

