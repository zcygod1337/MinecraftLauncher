#ifndef _DOWNLOAD_hpp
#define _DOWNLOAD_hpp

//QWQ
namespace download{
	void download_version(std::string version){
		std::string command=".\\download_version.py "+version;
		system(command.c_str());
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

