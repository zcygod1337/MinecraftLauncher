import json.readVer;
import org.json.JSONArray;
import org.json.JSONObject;
import swing.SwingMain;
import tools.LocalFileCreate;

import java.io.IOException;
import java.util.Objects;

public class Main {
    public static void main(String[] args) {
        LocalFileCreate.createUsernameTxt();
        SwingMain.startSwing();

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            try {
                LocalFileCreate.fileWriter.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }));
    }
}
