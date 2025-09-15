package tools;

import java.net.URL;

public class ResourcesIO {
    public static String findFile(String file) {
        if (file != null) {
            URL targets = ResourcesIO.class.getClassLoader().getResource(file);
            if (targets != null) {
                return targets.getFile();
            } else {
                return null;
            }
        }
        return null;
    }
}
