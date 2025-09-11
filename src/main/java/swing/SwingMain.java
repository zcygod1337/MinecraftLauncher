package swing;

import cpp.Connect;

import javax.swing.*;
import java.awt.*;

/**
 * @author XeContrast
 * 老子等你的CPP代码你人呢我操你妈的
 */
public class SwingMain {
    public static String username = "";
    public static void startSwing() {
        JFrame jFrame = new JFrame();
        jFrame.setLocation(570, 320);
        jFrame.setSize(570, 320);
        jFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        jFrame.setTitle("Minecraft Launcher");
        Container container = jFrame.getContentPane();
        JLabel jLabel = new JLabel("Username: " + username);
        jLabel.setBounds(60, 10, 80, 30);
        container.add(jLabel);
        JButton jButton = new JButton("Start");
        container.add(jButton, BorderLayout.SOUTH);
        JButton setUsername = new JButton("SetUsername");
        container.add(setUsername,BorderLayout.NORTH);
        jFrame.setVisible(true);

        setUsername.addActionListener(e -> {
            String input = JOptionPane.showInputDialog(null, "SetUsername");
            if (input != null) {
                username = input.trim();
                jLabel.setText("Username: " + username);
            }
        });

        jButton.addActionListener(e -> {
            if (username != null && !username.isEmpty()) {
                Connect.connectCppApp(username);
            } else {
                JOptionPane.showMessageDialog(null, "NullName");
            }
        });
    }
}