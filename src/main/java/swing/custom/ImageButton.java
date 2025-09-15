package swing.custom;

import javax.imageio.IIOException;
import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.InputStream;

public class ImageButton extends Component {
    private Image image;

    public ImageButton(String file) {
        try (InputStream inputStream = getClass().getClassLoader().getResourceAsStream(file)) {
            if (inputStream == null) {
                System.out.println("NoFind");
                return;
            }
            image = ImageIO.read(inputStream);
        } catch (IIOException iioException) {
            JOptionPane.showMessageDialog(null,"存储空间不足");
        } catch (Exception e) {
            e.printStackTrace();
            image = null;
        }
    }

    @Override
    public void paint(Graphics g) {
        Graphics2D g2d = (Graphics2D) g.create();
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2d.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
        g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        try {
            g2d.drawImage(image, 0, 0, this.getWidth(), this.getHeight(), null);
        } finally {
            g2d.dispose();
        }
    }
}
