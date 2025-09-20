package json;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class readVer {
    public static JSONObject getJson() {
        try {
            URL mojangURL = new URL("https://launchermeta.mojang.com/mc/game/version_manifest.json");

            HttpURLConnection httpURLConnection = (HttpURLConnection) mojangURL.openConnection();
            httpURLConnection.setRequestMethod("GET");
            httpURLConnection.setRequestProperty("Accept", "application/json");
            int responseCode = httpURLConnection.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 读取响应输入流
                BufferedReader reader = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));
                String line;
                StringBuilder response = new StringBuilder();

                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }

                return new JSONObject(String.valueOf(response));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }
}
