package cpp;

import tools.ResourcesIO;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Paths;

public class Connect {
    public static void connectCppApp(String filename) {
        new Thread(() -> {
            ProcessBuilder pb = new ProcessBuilder(ResourcesIO.findFile(filename));
            pb.directory(new File("F:\\FDP\\MinecraftLauncher\\src\\main\\resources"));
            Process p;
            try {
                p = pb.start();


                Thread outputThread = getThread(p.getInputStream(), "INFO: ");

                // 创建单独线程处理错误流
                Thread errorThread = getThread(p.getErrorStream(), "ERROR: ");

                // 在主线程中处理输入
                try (BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(p.getOutputStream()));
                     BufferedReader consoleReader = new BufferedReader(new InputStreamReader(System.in))) {
                    String line;
                    while ((line = consoleReader.readLine()) != null) {
                        writer.write(line);
                        writer.newLine();
                        writer.flush();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }

                // 等待进程结束
                p.waitFor();
                outputThread.join();
                errorThread.join();

            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }

    private static Thread getThread(InputStream p, String x) {
        Thread outputThread = new Thread(() -> {
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(p))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(x + line);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
        outputThread.start();
        return outputThread;
    }
}