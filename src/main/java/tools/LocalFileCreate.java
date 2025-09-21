package tools;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static swing.initGui.usernameList;

public class LocalFileCreate {
    public static BufferedWriter fileWriter;
    public static void createUsernameTxt() {
        Path path = Paths.get(".\\la");

        try {
            if (!Files.exists(path)) {
                Files.createDirectory(path);
            }
            fileWriter = new BufferedWriter(new FileWriter(".\\la\\username.txt",true));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void addUsername() {
        String line;
        try (BufferedReader reader = new BufferedReader(new FileReader(".\\la\\username.txt"))) {
            while ((line = reader.readLine()) != null) {
                StringBuilder stringBuilder = new StringBuilder(line);
                stringBuilder.delete(0,10);
                System.out.println(stringBuilder);
                usernameList.add(stringBuilder.toString());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
