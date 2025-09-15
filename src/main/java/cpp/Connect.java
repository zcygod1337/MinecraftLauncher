package cpp;

import tools.ResourcesIO;

import java.io.*;
import java.util.concurrent.TimeUnit;

public class Connect {
    public static void connectCppApp(String username) {
        new Thread(() -> {
            ProcessBuilder pb = new ProcessBuilder(ResourcesIO.findFile("main.exe"));
            pb.directory(new File("."));
            Process p = null;
            try {
                p = pb.start();
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream(),"GBK"))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        System.out.println(line + "\n");
                    }
                }

                try (BufferedReader reader = new BufferedReader(new InputStreamReader(p.getErrorStream(),"GBK"))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        System.out.println(line + "\n");
                    }
                }

                try (BufferedWriter reader = new BufferedWriter(new OutputStreamWriter(p.getOutputStream()))) {
                    try (BufferedReader reader1 = new BufferedReader(new InputStreamReader(System.in))) {
                        String line;
                        while ((line = reader1.readLine()) != null) {
                            reader.write(line);
                            reader.newLine();
                            reader.flush();
                        }
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                if (p != null) {
                    p.destroy();
                    try {
                        boolean wait = p.waitFor(3, TimeUnit.SECONDS);
                        if (wait) {
                            p.destroyForcibly();
                        }
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }
}
