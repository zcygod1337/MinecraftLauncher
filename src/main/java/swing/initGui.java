package swing;

import cpp.Connect;
import swing.custom.ImageButton;
import swing.custom.LoginFrame;

import javax.swing.*;
import java.awt.event.*;

/**
 * @author XeContrast
 * 1% AICode
 */
public class initGui {
    public static int pages = 0;
    public static String username = "";
    static JFrame jFrame = new JFrame("Minecraft Launcher");
    private static final JPanel container = (JPanel) jFrame.getContentPane();
    private static ImageButton imageButton,imageButton1;
    private static JButton startButton,setUsername;
    private static JLabel page;
    public static JLabel usernameLabel;
    public static void init() {
        jFrame.setLocation(300, 200);
        jFrame.setSize(1200, 800);
        jFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        jFrame.setLayout(null);
    }

    public static void refresh() {
        if (pages != 0) {
            startButton.setVisible(false);
            setUsername.setVisible(false);
            usernameLabel.setVisible(false);
        } else {
            startButton.setVisible(true);
            setUsername.setVisible(true);
            usernameLabel.setVisible(true);
        }
    }

    public static void showImage() {
        imageButton = new ImageButton("R.png");
        imageButton.setBounds(10,5,50,50);
        jFrame.add(imageButton);

        imageButton1 = new ImageButton("RM.png");
        imageButton1.setBounds(jFrame.getWidth() - 70,5,50,50);
        jFrame.add(imageButton1);

        new Thread(() -> {
            while (true) {
                imageButton.setLocation(10,5);
                imageButton1.setLocation(jFrame.getWidth() - 70,5);
                if (pages <= 0) {
                    pages = 0;
                }
            }
        }).start();

        imageButton.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                pages -= 1;
            }
        });

        imageButton1.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                pages += 1;
            }
        });
    }

    public static void showStartButton() {
        startButton = new JButton("Start");
        startButton.setBounds(jFrame.getWidth() - 180,jFrame.getHeight() - 80,120,40);
        container.add(startButton);

        startButton.addActionListener(e -> {
            if (username != null && !username.isEmpty()) {
                Connect.connectCppApp(username);
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
