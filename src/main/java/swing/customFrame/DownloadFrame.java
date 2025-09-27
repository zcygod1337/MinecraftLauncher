package swing.customFrame;

import cpp.Connect;
import json.readVer;
import org.json.JSONArray;
import org.json.JSONObject;
import tools.ResourcesIO;

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

        setLayout(new BoxLayout(getContentPane(), BoxLayout.Y_AXIS));
//        container.set(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        JPanel typePanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JLabel typeLabel = new JLabel("版本类型:");
        JComboBox<String> verType = new JComboBox<>(new String[]{"snapshot", "release"});
        typePanel.add(typeLabel);
        typePanel.add(verType);

        JPanel versionPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JLabel versionLabel = new JLabel("版本号:");
        JComboBox<String> verSelection = new JComboBox<>();
        versionPanel.add(versionLabel);
        versionPanel.add(verSelection);

        loadVersionData(verType, verSelection);

        verType.addItemListener(e -> {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                updateVersionSelection(verType, verSelection);
            }
        });

        container.add(typePanel);
        container.add(Box.createRigidArea(new Dimension(0, 5)));
        container.add(versionPanel);
        container.add(Box.createVerticalGlue());

        JPanel buttonPanel = new JPanel();
        JButton confirmButton = new JButton("确定");
        buttonPanel.add(confirmButton);
        container.add(Box.createRigidArea(new Dimension(0, 20)));
        container.add(buttonPanel);

        confirmButton.addActionListener(e -> {
            if (verSelection.getSelectedItem() != null) {
                System.out.println(ResourcesIO.findFile("main.exe") + "-download" + verSelection.getSelectedItem().toString());
                Connect.connectCppApp(ResourcesIO.findFile("main.exe"), "-download", verSelection.getSelectedItem().toString());
            }
        });
    }

    private void loadVersionData(JComboBox<String> verType, JComboBox<String> verSelection) {
        if (verType.getSelectedItem() == null)
            return;
        JSONObject jsonObject = readVer.getJson("https://launchermeta.mojang.com/mc/game/version_manifest.json");
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
        // 默认选择第一个版本
        if (verSelection.getItemCount() > 0) {
            verSelection.setSelectedIndex(0);
        }
    }

    private void updateVersionSelection(JComboBox<String> verType, JComboBox<String> verSelection) {
        String selectedType = (String) verType.getSelectedItem();
        verSelection.removeAllItems();

        JSONObject jsonObject = readVer.getJson("https://launchermeta.mojang.com/mc/game/version_manifest.json");
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