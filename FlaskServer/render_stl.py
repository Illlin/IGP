import sys
import vtkplotlib as vpl
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow
from PyQt5.QtCore import Qt
from stl.mesh import Mesh

from cube import generate_cube, emotion_cube

class SliderWidget(QWidget):
    def __init__(self, slider_dict):
        self.slider_dict = slider_dict
        super().__init__()
        self.sliders = {}
        layout = QVBoxLayout()
        for key, values in slider_dict.items():
            slider_layout = QHBoxLayout()
            label = QLabel(key)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(values[0], values[1])
            #slider.setValue((values[1] - values[0]) / 2)
            value_label = QLabel(str(slider.value()))
            slider_layout.addWidget(label)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(value_label)
            layout.addLayout(slider_layout)
            self.sliders[key] = (slider, value_label)

            slider.valueChanged.connect(lambda value, label=value_label: label.setText(str(value)))

        self.setLayout(layout)

    def get_slider_values(self):
        values = {}
        for key, (slider, _) in self.sliders.items():
            values[key] = slider.value()/ self.slider_dict[key][2]
        return values

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path="cube.stl"
        slider_dict = {
            "height": [0, 100, 100],
            "smooth": [0, 5, 1],
            "curve": [0, 100, 100], 
            "width":[0,128,1],
            "depth":[0,100,100],
            "highpass":[0,100,100],
            "lowpass":[0,100,100],
            "noise":[0,100,100]
            }
        slider_dict = {
            "sadness": [0, 100, 100],
            "joy": [0, 100, 100],
            "fear": [0, 100, 100],
            "disgust": [0, 100, 100],
            "anger": [0, 100, 100],
            }
        self.widget = SliderWidget(slider_dict)
        button = QPushButton("Gen Cube")
        button.clicked.connect(self.on_button_click)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox = QVBoxLayout(central_widget)

        self.figure = vpl.QtFigure()
        vbox.addWidget(self.widget)
        vbox.addWidget(button)
        vbox.addWidget(self.figure)

        
        self.figure.show()


    def on_button_click(self):
        print(self.widget.get_slider_values())
        emotion_cube("FlaskServer/test_files/test_happy.wav", "cube.stl", self.widget.get_slider_values())
        mesh = Mesh.from_file("cube.stl")
        a = []
        for i in self.figure.plots:
            a.append(i)
        for i in a:
            self.figure.remove_plot(i)
        vpl.mesh_plot(mesh, fig=self.figure)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

