package swing.customFrame;

import tools.LocalFileCreate;

import javax.swing.*;
import java.awt.*;
import java.io.IOException;

import static swing.initGui.*;

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
            } else {
                usernameList.add(input.getText());
                usernameB.addItem(input.getText());
                try {
                    LocalFileCreate.fileWriter.write("username: " + username);
                    LocalFileCreate.fileWriter.newLine();
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
                usernameLabel.setText("Username: " + username);
            }
        });

        new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
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
