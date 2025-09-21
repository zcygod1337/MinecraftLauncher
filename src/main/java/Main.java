import swing.SwingMain;
import tools.LocalFileCreate;
import tools.ResourcesIO;

import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        try {
            ResourcesIO.copyResources("lib", Paths.get(".\\la"));
        } catch (IOException | URISyntaxException e) {
            e.printStackTrace();
        }
        LocalFileCreate.addUsername();
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
