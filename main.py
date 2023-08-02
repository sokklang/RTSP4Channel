import cv2
import json
import urllib.parse
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget, QLineEdit, QPushButton, QFileDialog

class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)
        self.image_label = QLabel()
        layout = QGridLayout()
        layout.addWidget(self.image_label, 0, 0, 1, 1)
        self.setLayout(layout)

    def set_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = channel * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        layout = QGridLayout()

        # List to store the video widgets
        self.video_widgets = []

        # Add four video widgets to the layout
        for row in range(2):
            for col in range(2):
                video_widget = VideoWidget()
                layout.addWidget(video_widget, row, col)
                self.video_widgets.append(video_widget)

        # Configuration fields
        self.config_line_edit = QLineEdit()
        self.load_config_button = QPushButton("Load Config")
        self.load_config_button.clicked.connect(self.load_config)
        self.start_stream_button = QPushButton("Start Stream")
        self.start_stream_button.clicked.connect(self.start_stream)

        # Add configuration fields to layout
        layout.addWidget(self.config_line_edit, 2, 0, 1, 2)
        layout.addWidget(self.load_config_button, 3, 0)
        layout.addWidget(self.start_stream_button, 3, 1)

        self.setLayout(layout)

        self.caps = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)

        self.file_dialog = QFileDialog()

    def load_config(self):
        # Open the file dialog to select the configuration file
        file_dialog_options = QFileDialog.Options()
        file_dialog_options |= QFileDialog.ReadOnly

        file_urls, _ = self.file_dialog.getOpenFileUrls(self, "Load Config", QUrl(), "JSON Files (*.json)", options=file_dialog_options)

        if file_urls:
            file_path = file_urls[0].toLocalFile()
            self.config_line_edit.setText(file_path)

    def start_stream(self):
        # Read configuration from the input field
        config_path = self.config_line_edit.text()

        # Read configuration from JSON file
        with open(config_path) as config_file:
            config = json.load(config_file)

        # Iterate over the channels in the configuration
        for channel_config in config.get("channels", []):
            username = channel_config.get("username")
            password = channel_config.get("password")
            xvr_ip = channel_config.get("xvr_ip")
            channel = channel_config.get("channel")
            stream_type = channel_config.get("stream_type")

            # URL-encode the password
            encoded_password = urllib.parse.quote(password, safe='')

            # RTSP URL for the desired channel and stream type
            rtsp_url = f"rtsp://{username}:{encoded_password}@{xvr_ip}/cam/realmonitor?channel={channel}&subtype={stream_type}"

            cap = cv2.VideoCapture(rtsp_url)

            # Check if the stream is opened successfully
            if not cap.isOpened():
                print(f"Failed to open the RTSP stream for channel {channel}")
                continue

            self.caps.append(cap)

        self.timer.start(30)

    def update_frames(self):
        for i, cap in enumerate(self.caps):
            ret, frame = cap.read()

            if not ret:
                print(f"Failed to retrieve frame from stream {i+1}")
                continue

            # Resize the frame to fit the video widget
            resized_frame = cv2.resize(frame, (self.video_widgets[i].width(), self.video_widgets[i].height()))

            self.video_widgets[i].set_frame(resized_frame)

    def keyPressEvent(self, event):
        # Capture keyboard input
        key = event.key()

        # Press 'q' to exit
        if key == Qt.Key_Q:
            for cap in self.caps:
                cap.release()
            self.timer.stop()
            self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
