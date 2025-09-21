package tools;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

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

    public static InputStream findFileStream(String file) {
        if (file != null) {
            return ResourcesIO.class.getClassLoader().getResourceAsStream(file);
        }
        return null;
    }

    public static void copyResources(String sourceDir, Path targetPath) throws IOException, URISyntaxException {
        // 获取resources目录的URL
        URL resourceUrl = ResourcesIO.class.getClassLoader().getResource(sourceDir);
        if (resourceUrl == null) {
            throw new IOException("Resources directory not found: " + sourceDir);
        }

        Path sourcePath = Paths.get(resourceUrl.toURI());

        // 确保目标目录存在
        Files.createDirectories(targetPath);

        // 复制整个目录
        Files.walk(sourcePath)
                .forEach(source -> {
                    try {
                        Path destination = targetPath.resolve(sourcePath.relativize(source));
                        if (Files.isDirectory(source)) {
                            Files.createDirectories(destination);
                        } else {
                            Files.copy(source, destination, StandardCopyOption.REPLACE_EXISTING);
                        }
                    } catch (IOException e) {
                        throw new RuntimeException("Failed to copy resource: " + source, e);
                    }
                });
    }
}
