package swing.customFrame;

import json.readVer;
import org.json.JSONArray;
import org.json.JSONObject;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ItemEvent;

public class DownloadFrame extends JDialog {
    public DownloadFrame(JFrame jFrame) {
        super(jFrame, "Download", true);
        Container container = getContentPane();

        setSize(600, 200);
        setLocationRelativeTo(jFrame);
        setResizable(false);
        setLayout(new FlowLayout(FlowLayout.LEFT, 10, 10));

        JComboBox<String> verType = new JComboBox<>(new String[]{"snapshot", "release"});
        JComboBox<String> verSelection = new JComboBox<>();

        loadVersionData(verType, verSelection);

        verType.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                updateVersionSelection(verType, verSelection);
            }
        });

        container.add(new JLabel("版本类型:"));
        container.add(verType);
        container.add(new JLabel("版本号:"));
        container.add(verSelection);
    }

    private void loadVersionData(JComboBox<String> verType, JComboBox<String> verSelection) {
        JSONObject jsonObject = readVer.getJson();
        if (jsonObject != null) {
            JSONArray jsonArray = jsonObject.getJSONArray("versions");
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject version = jsonArray.getJSONObject(i);
                String type = version.getString("type");
                String id = version.getString("id");

                if ("release".equals(type)) {
                    verSelection.addItem(id);
                } else if ("snapshot".equals(type) && verType.getSelectedItem().equals("snapshot")) {
                    verSelection.addItem(id);
                }
            }
        }

        if (verSelection.getItemCount() > 0) {
            verSelection.setSelectedIndex(0);
        }
    }

    private void updateVersionSelection(JComboBox<String> verType, JComboBox<String> verSelection) {
        String selectedType = (String) verType.getSelectedItem();
        verSelection.removeAllItems();

        JSONObject jsonObject = readVer.getJson();
        if (jsonObject != null) {
            JSONArray jsonArray = jsonObject.getJSONArray("versions");
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject version = jsonArray.getJSONObject(i);
                String type = version.getString("type");
                String id = version.getString("id");

                if (selectedType.equals(type)) {
                    verSelection.addItem(id);
                }
            }
        }

        if (verSelection.getItemCount() > 0) {
            verSelection.setSelectedIndex(0);
        }
    }
}