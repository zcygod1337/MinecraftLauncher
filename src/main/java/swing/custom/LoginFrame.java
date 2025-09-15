package swing.custom;

import javax.swing.*;
import java.awt.*;

import static swing.initGui.username;
import static swing.initGui.usernameLabel;

public class LoginFrame extends JDialog {
    public LoginFrame(JFrame parent) {
        super(parent,"Login",true);

        Container jPanel = getContentPane();

        setSize(300,200);
        setLocationRelativeTo(parent);
        setResizable(false);

        setLayout(null);

        JRadioButton crk = new JRadioButton("Crk");
        crk.setBounds(getWidth() / 2 - 60,10,60,30);
        crk.setSelected(true);
        JRadioButton online = new JRadioButton("Online");
        online.setBounds(getWidth() / 2,10,80,30);

        ButtonGroup buttonGroup = new ButtonGroup();
        buttonGroup.add(crk);
        buttonGroup.add(online);

        JLabel text = new JLabel("Username");
        text.setBounds(getWidth() / 2 - 60,60,120,20);
        JTextField input = new JTextField(8);
        input.setBounds(getWidth() / 2 - 60,80,120,20);
        JButton enter = new JButton("Add");
        enter.setBounds(getWidth() / 2 - 60,120,120,40);

        jPanel.add(text);
        jPanel.add(enter);
        jPanel.add(input);
        jPanel.add(crk);
        jPanel.add(online);

        enter.addActionListener(e -> {
            if (input.getText().isEmpty()) {
                int answer = JOptionPane.showConfirmDialog(null,"Name is empty","OK?",JOptionPane.OK_CANCEL_OPTION);
                if (answer == 0) {
                    dispose();
                }
            } else {
                username = input.getText();
                usernameLabel.setText("Username: " + username);
                if (crk.isSelected())
                    dispose();
            }
        });

        new Thread(() -> {
            while (true) {
                if (crk.isSelected()) {
                    text.setVisible(true);
                    input.setVisible(true);
                } else {
                    text.setVisible(false);
                    input.setVisible(false);
                }
            }
        }).start();
    }
}
