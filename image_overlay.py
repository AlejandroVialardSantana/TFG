import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QSlider, QLabel, QGraphicsView, 
                             QGraphicsScene, QGraphicsPixmapItem, QLineEdit)
from PyQt5.QtGui import QPixmap, QImage, QCursor, QTransform
from PyQt5.QtCore import Qt, QPointF
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

class DraggablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)
        self.setFlag(QGraphicsPixmapItem.ItemIsSelectable, True)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self.rotation = 0
        self.flipped = False

    def mousePressEvent(self, event):
        self.setCursor(QCursor(Qt.ClosedHandCursor))
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.OpenHandCursor))
        super().mouseReleaseEvent(event)

    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360
        self.setRotation(self.rotation)

    def flip(self):
        self.flipped = not self.flipped
        self.setTransform(QTransform().scale(-1 if self.flipped else 1, 1))

class ImageCompositorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Compositor')
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Área de visualización de la imagen
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        main_layout.addWidget(self.view)

        # Controles
        controls_layout = QHBoxLayout()
        
        load_bg_button = QPushButton('Cargar Fondo')
        load_bg_button.clicked.connect(self.load_background)
        controls_layout.addWidget(load_bg_button)

        load_dir_button = QPushButton('Cargar Directorio')
        load_dir_button.clicked.connect(self.load_image_directory)
        controls_layout.addWidget(load_dir_button)

        next_image_button = QPushButton('Siguiente Imagen')
        next_image_button.clicked.connect(self.next_image)
        controls_layout.addWidget(next_image_button)

        save_button = QPushButton('Guardar en Directorio')
        save_button.clicked.connect(self.save_image)
        controls_layout.addWidget(save_button)

        # Añadir controles para rotación y volteo
        rotate_left_button = QPushButton('Rotar Izquierda')
        rotate_left_button.clicked.connect(lambda: self.rotate_overlay(-90))
        controls_layout.addWidget(rotate_left_button)

        rotate_right_button = QPushButton('Rotar Derecha')
        rotate_right_button.clicked.connect(lambda: self.rotate_overlay(90))
        controls_layout.addWidget(rotate_right_button)

        flip_button = QPushButton('Voltear')
        flip_button.clicked.connect(self.flip_overlay)
        controls_layout.addWidget(flip_button)

        reset_zoom_button = QPushButton('Restablecer Zoom')
        reset_zoom_button.clicked.connect(self.reset_zoom)
        controls_layout.addWidget(reset_zoom_button)

        main_layout.addLayout(controls_layout)

        # Parámetros
        params_layout = QHBoxLayout()

        # Umbral
        threshold_layout = QVBoxLayout()
        threshold_layout.addWidget(QLabel('Umbral:'))
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(140)
        self.threshold_slider.valueChanged.connect(self.update_image)
        threshold_layout.addWidget(self.threshold_slider)
        self.threshold_input = QLineEdit('140')
        self.threshold_input.textChanged.connect(self.update_threshold)
        threshold_layout.addWidget(self.threshold_input)
        params_layout.addLayout(threshold_layout)

        # Desenfoque
        blur_layout = QVBoxLayout()
        blur_layout.addWidget(QLabel('Desenfoque:'))
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(0, 50)
        self.blur_slider.setValue(15)
        self.blur_slider.valueChanged.connect(self.update_image)
        blur_layout.addWidget(self.blur_slider)
        self.blur_input = QLineEdit('15')
        self.blur_input.textChanged.connect(self.update_blur)
        blur_layout.addWidget(self.blur_input)
        params_layout.addLayout(blur_layout)

        # Opacidad
        opacity_layout = QVBoxLayout()
        opacity_layout.addWidget(QLabel('Opacidad:'))
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.update_image)
        opacity_layout.addWidget(self.opacity_slider)
        self.opacity_input = QLineEdit('100')
        self.opacity_input.textChanged.connect(self.update_opacity)
        opacity_layout.addWidget(self.opacity_input)
        params_layout.addLayout(opacity_layout)

        # Escala
        scale_layout = QVBoxLayout()
        scale_layout.addWidget(QLabel('Escala (%):'))
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(10, 200)
        self.scale_slider.setValue(100)
        self.scale_slider.valueChanged.connect(self.update_image)
        scale_layout.addWidget(self.scale_slider)
        self.scale_input = QLineEdit('100')
        self.scale_input.textChanged.connect(self.update_scale)
        scale_layout.addWidget(self.scale_input)
        params_layout.addLayout(scale_layout)

        main_layout.addLayout(params_layout)

        # Variables para almacenar las imágenes y parámetros
        self.background_image = None
        self.overlay_images = []
        self.current_overlay_index = 0
        self.overlay_item = None
        self.save_directory = ""
        self.frame_count = 0

    def reset_zoom(self):
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def load_background(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen de fondo", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.background_image = Image.open(file_name).convert("RGBA")
            self.update_image()

    def load_image_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de imágenes")
        if directory:
            self.overlay_images = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.current_overlay_index = 0
            self.update_image()

    def next_image(self):
        if self.overlay_images:
            self.save_overlay_position()
            self.save_image()
            self.current_overlay_index = (self.current_overlay_index + 1) % len(self.overlay_images)
            self.update_image()

    def update_image(self):
        if self.background_image and self.overlay_images:
            self.scene.clear()
            bg_pixmap = QPixmap.fromImage(self.pil_to_qimage(self.background_image))
            self.scene.addPixmap(bg_pixmap)

            overlay = self.compose_overlay()
            overlay_pixmap = QPixmap.fromImage(self.pil_to_qimage(overlay))

            # Siempre crear un nuevo DraggablePixmapItem
            self.overlay_item = DraggablePixmapItem(overlay_pixmap)
            self.scene.addItem(self.overlay_item)

            # Si había una posición anterior, intentamos mantenerla
            if hasattr(self, 'last_overlay_position'):
                self.overlay_item.setPos(self.last_overlay_position)

            self.scene.setSceneRect(self.scene.itemsBoundingRect())

    def compose_images(self):
        composite = self.background_image.copy()
        overlay = self.compose_overlay()
        if hasattr(self, 'last_overlay_position'):
            position = self.last_overlay_position
            composite.paste(overlay, (int(position.x()), int(position.y())), overlay)
        else:
            composite.paste(overlay, (0, 0), overlay)
        return composite
    
    def save_overlay_position(self):
        if self.overlay_item:
            self.last_overlay_position = self.overlay_item.pos()

    def compose_overlay(self):
        overlay = Image.open(self.overlay_images[self.current_overlay_index]).convert("RGBA")
        
        # Redimensionar la imagen superpuesta
        scale_factor = self.scale_slider.value() / 100.0
        new_size = (int(overlay.width * scale_factor), int(overlay.height * scale_factor))
        overlay_resized = overlay.resize(new_size, Image.LANCZOS)

        # Aplicar rotación y volteo
        if hasattr(self, 'overlay_item') and self.overlay_item:
            if self.overlay_item.rotation != 0:
                overlay_resized = overlay_resized.rotate(-self.overlay_item.rotation, expand=True)
            if self.overlay_item.flipped:
                overlay_resized = overlay_resized.transpose(Image.FLIP_LEFT_RIGHT)

        # Crear una máscara basada en el brillo
        gray_image = overlay_resized.convert("L")
        threshold = self.threshold_slider.value()
        mask = gray_image.point(lambda p: p > threshold and 255)

        # Desenfocar los bordes de la máscara
        blur_radius = self.blur_slider.value()
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        # Ajustar la opacidad
        opacity = self.opacity_slider.value() / 100.0
        overlay_resized.putalpha(Image.blend(Image.new('L', overlay_resized.size, 0), mask, opacity))

        return overlay_resized

    def save_image(self):
        if not self.save_directory:
            self.save_directory = QFileDialog.getExistingDirectory(self, "Seleccionar directorio para guardar")

        if self.save_directory:
            try:
                composite = self.compose_images()
                composite_gray = composite.convert("L")
                file_name = f"frame{self.frame_count:04d}.png"
                file_path = os.path.join(self.save_directory, file_name)
                composite_gray.save(file_path)
                self.frame_count += 1
            except Exception as e:
                print(f"Error al guardar la imagen: {e}")

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.view.scale(1.1, 1.1)
        else:
            self.view.scale(0.9, 0.9)

    def resizeEvent(self, event):
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    @staticmethod
    def pil_to_qimage(pil_image):
        if pil_image.mode == "RGB":
            r, g, b = pil_image.split()
            pil_image = Image.merge("RGB", (b, g, r))
        elif pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            pil_image = Image.merge("RGBA", (b, g, r, a))
        
        im_arr = np.array(pil_image)
        height, width, channel = im_arr.shape
        bytes_per_line = channel * width
        return QImage(im_arr.data, width, height, bytes_per_line, QImage.Format_RGBA8888)

    def update_threshold(self, value):
        try:
            self.threshold_input.setText(str(value))
            self.save_overlay_position()
            self.update_image()
        except ValueError:
            pass

    def update_blur(self, value):
        try:
            self.blur_input.setText(str(value))
            self.save_overlay_position()
            self.update_image()
        except ValueError:
            pass

    def update_opacity(self, value):
        try:
            self.opacity_input.setText(str(value))
            self.save_overlay_position()
            self.update_image()
        except ValueError:
            pass

    def update_scale(self, value):
        try:
            self.scale_input.setText(str(value))
            self.save_overlay_position()
            self.update_image()
        except ValueError:
            pass

    def rotate_overlay(self, angle):
        if self.overlay_item:
            self.overlay_item.rotate(angle)
            self.save_overlay_position()
            self.update_image()

    def flip_overlay(self):
        if self.overlay_item:
            self.overlay_item.flip()
            self.save_overlay_position()
            self.update_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageCompositorApp()
    ex.show()
    sys.exit(app.exec_())