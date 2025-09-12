package swing;

import static swing.initGui.container;
import static swing.initGui.jFrame;

/**
 * @author XeContrast
 * 老子等你的CPP代码你人呢我操你妈的
 */
public class SwingMain {
    public static void startSwing() {
        initGui.init();
        initGui.showImage();
        switch (initGui.pages) {
            case 0:
                initGui.setUsernameButton();
                initGui.showStartButton();
                initGui.showPages();
                break;
        }
        jFrame.setVisible(true);
    }
}