package swing;

import static swing.initGui.jFrame;

/**
 * @author XeContrast
 * 老子等你的CPP代码你人呢我操你妈的
 */
public class SwingMain {
    public static void startSwing() {
        initGui.init();
        initGui.showDownloadButton();
        initGui.showPages();
        initGui.showStartButton();
        initGui.setUsernameButton();
        jFrame.setVisible(true);
    }
}