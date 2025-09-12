package swing;

import cpp.Connect;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;

/**
 * @author XeContrast
 * 1% AICode
 */
public class initGui {
    public static int pages = 0;
    public static String username = "";
    static JFrame jFrame = new JFrame("Minecraft Launcher");
    static Container container = jFrame.getContentPane();
    public static void init() {
        jFrame.setLocation(570, 320);
        jFrame.setSize(570, 320);
        jFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        jFrame.setLayout(null);
        jFrame.setVisible(true);
    }

    public static void showStartButton() {
        JButton jButton = new JButton("Start");
        jButton.setBounds(jFrame.getWidth() - 180,jFrame.getHeight() - 80,120,40);
        container.add(jButton);

        jButton.addActionListener(e -> {
            if (username != null && !username.isEmpty()) {
                Connect.connectCppApp(username);
            } else {
                JOptionPane.showMessageDialog(null, "NullName");
            }
        });

        jFrame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                jButton.setLocation(jFrame.getWidth() - 140,jFrame.getHeight() - 80);
            }
        });
    }

    public static void showPages() {
        JLabel text = new JLabel("Pages: " + pages);
        text.setBounds(jFrame.getWidth() / 2 - 40,-20,80,80);
        container.add(text);

        jFrame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                text.setLocation(jFrame.getWidth() / 2 - 40,-20);
                text.setText("Pages: " + pages);
            }
        });
    }

    public static void setUsernameButton() {
        JLabel jLabel = new JLabel("Username: " + username);
        jLabel.setBounds(10, 10, 80, 30);
        container.add(jLabel);

        JButton setUsername = new JButton("SetUsername");
        setUsername.setBounds(jFrame.getWidth() - 280,jFrame.getHeight() - 80,120,40);
        container.add(setUsername);

        setUsername.addActionListener(e -> {
            String input = JOptionPane.showInputDialog(null, "SetUsername");
            if (input != null) {
                username = input.trim();
                jLabel.setText("Username: " + username);
            }
        });

        jFrame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                setUsername.setLocation(jFrame.getWidth() - 280,jFrame.getHeight() - 80);
            }
        });
    }
}
