package tools;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class LocalFileCreate {
    public static BufferedWriter fileWriter;
    public static void createUsernameTxt() {
        Path path = Paths.get(".\\la");

        try {
            if (!Files.exists(path)) {
                Files.createDirectory(path);
            }
            fileWriter = new BufferedWriter(new FileWriter(".\\la\\username.txt"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
