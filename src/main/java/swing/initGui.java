package swing;

import cpp.Connect;
import swing.customFrame.DownloadFrame;
import swing.customFrame.LoginFrame;
import tools.ResourcesIO;

import javax.swing.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.List;

/**
 * @author XeContrast
 * 1% AICode
 */
public class initGui {
    public static int pages = 0;
    static JFrame jFrame = new JFrame("Minecraft Launcher");
    private static final JPanel container = (JPanel) jFrame.getContentPane();
    private static JButton startButton,setUsername,downloadButton;
    private static JLabel page;
    public static JLabel usernameLabel;
    public static List<String> usernameList = new ArrayList<>();
    public static final JComboBox<Object> usernameB = new JComboBox<>();
    public static String username = "";
    public static void init() {
        jFrame.setLocation(300, 200);
        jFrame.setSize(1200, 800);
        jFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        jFrame.setLayout(null);
    }

    public static void usernameBox() {
        usernameB.setBounds(10, 10, 120, 30);
        for (String string : usernameList) {
            usernameB.removeAll();
            usernameB.addItem(string);
        }
        usernameB.setVisible(true);
        container.add(usernameB);
        if (usernameB.getSelectedItem() != null) {
            username = usernameB.getSelectedItem().toString();
        }
        usernameB.addItemListener(e -> {
            username = usernameB.getSelectedItem().toString();
            usernameLabel.setText("Username: " + username);
        });
    }

    public static void showDownloadButton() {
        downloadButton = new JButton("Download");
        downloadButton.setBounds(jFrame.getWidth() - 420,jFrame.getHeight() - 80,120,40);
        container.add(downloadButton);

        downloadButton.addActionListener(e -> {
            DownloadFrame downloadFrame = new DownloadFrame(jFrame);
            downloadFrame.setVisible(true);
        });

        jFrame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                downloadButton.setLocation(jFrame.getWidth() - 420,jFrame.getHeight() - 80);
            }
        });
    }

    public static void showStartButton() {
        startButton = new JButton("Start");
        startButton.setBounds(jFrame.getWidth() - 140,jFrame.getHeight() - 80,120,40);
        container.add(startButton);

        startButton.addActionListener(e -> {
            if (username != null && !username.isEmpty()) {
                Connect.connectCppApp(ResourcesIO.findFile("main.exe"),"-run","1.12.2","-username",username);
            } else {
                JOptionPane.showMessageDialog(null, "NullName");
            }
        });

        jFrame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                startButton.setLocation(jFrame.getWidth() - 140,jFrame.getHeight() - 80);
            }
        });
    }

    public static void showPages() {
        page = new JLabel("Pages: " + pages);
        page.setBounds(jFrame.getWidth() / 2 - 40, -20, 80, 80);
        container.add(page);

        jFrame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                page.setLocation(jFrame.getWidth() / 2 - 40, -20);
            }
        });

        new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                page.setText("Pages: " + pages);
            }
        }).start();
    }

    public static void setUsernameButton() {
        usernameLabel = new JLabel("Username: " + username);
        usernameLabel.setBounds(10, 10, 200, 100);
        container.add(usernameLabel);

        setUsername = new JButton("Login");
        setUsername.setBounds(jFrame.getWidth() - 280,jFrame.getHeight() - 80,120,40);
        container.add(setUsername);

        setUsername.addActionListener(e -> {
            LoginFrame loginFrame = new LoginFrame(jFrame);
            loginFrame.setVisible(true);
        });

        jFrame.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentResized(ComponentEvent e) {
                setUsername.setLocation(jFrame.getWidth() - 280,jFrame.getHeight() - 80);
            }
        });
    }
}
