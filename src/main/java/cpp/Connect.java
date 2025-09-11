package cpp;

import java.io.IOException;

public class Connect {
    public static void connectCppApp(String username) {
        try {
            ProcessBuilder pb = new ProcessBuilder("srcOther/main.exe",username);
            pb.redirectErrorStream(true);
            pb.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
