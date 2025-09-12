package swing;

import cpp.Connect;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;

/**
 * @author XeContrast
 * AICode 5%
 * 老子等你的CPP代码你人呢我操你妈的
 */
public class SwingMain {
    public static String username = "";
    public static void startSwing() {
        //Show GUI's Setting
        JFrame jFrame = new JFrame();
        jFrame.setLocation(570, 320);
        jFrame.setSize(570, 320);
        jFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        jFrame.setTitle("Minecraft Launcher");
        jFrame.setLayout(null);
        jFrame.setVisible(true);

        Container container = jFrame.getContentPane();

        //Show Text
        JLabel jLabel = new JLabel("Username: " + username);
        jLabel.setBounds(10, 10, 80, 30);
        container.add(jLabel);

        //Start Button
        JButton jButton = new JButton("Start");
        jButton.setBounds(jFrame.getWidth() - 180,jFrame.getHeight() - 100,120,40);
        container.add(jButton);

        //SetUsername Button
        JButton setUsername = new JButton("SetUsername");
        setUsername.setBounds(jFrame.getWidth() - 240,jFrame.getHeight() - 100,120,40);
        container.add(setUsername);

        //Update Start Button XYZ
        jFrame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                jButton.setLocation(jFrame.getWidth() - 140,jFrame.getHeight() - 80);
                setUsername.setLocation(jFrame.getWidth() - 280,jFrame.getHeight() - 80);
            }
        });

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