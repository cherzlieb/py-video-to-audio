import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QComboBox, QProgressBar, QRadioButton, QButtonGroup, QHBoxLayout
from PySide6.QtCore import QThread, Signal

class ConverterThread(QThread):
    """Thread für die Hintergrund-Konvertierung, damit die GUI nicht blockiert wird."""
    progress_signal = Signal(int)

    def __init__(self, input_folder, output_folder, audio_format, bitrate, sampling_rate):
        super().__init__()
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.audio_format = audio_format
        self.bitrate = bitrate
        self.sampling_rate = sampling_rate
        self.process = None  # Speichert den FFmpeg-Prozess für spätere Unterbrechung
        self.running = True  # Thread läuft standardmäßig weiter

    def run(self):
        mp4_files = [f for f in os.listdir(self.input_folder) if f.endswith(".mp4")]
        total_files = len(mp4_files)
        if total_files == 0:
            return

        for i, mp4_file in enumerate(mp4_files, start=1):
            if not self.running:  # Überprüfung für Abbrechen
                print("Konvertierung abgebrochen!")
                break
            mp4_path = os.path.join(self.input_folder, mp4_file)
            audio_path = os.path.join(self.output_folder, os.path.splitext(mp4_file)[0] + f".{self.audio_format}")

            command = [
                "ffmpeg",
                "-i", mp4_path,
                "-vn",
                "-acodec",
                "libmp3lame" if self.audio_format == "mp3" else "pcm_s16le" if self.audio_format == "wav" else "flac" if self.audio_format == "flac" else "libvorbis",
                "-b:a", self.bitrate,
                "-ar", self.sampling_rate,
                audio_path
            ]

            # Speichert den laufenden Prozess
            self.process = subprocess.Popen(command)

            self.process.wait()  # Wartet auf Abschluss
            self.progress_signal.emit(int((i / total_files) * 100))  # Fortschritt aktualisieren

    def stop(self):
        self.running = False  # Setzt running auf False, damit die Schleife stoppt
        if self.process:
            self.process.terminate()  # FFmpeg-Prozess beenden

class VideoConverter(QWidget):
    """GUI-Anwendung zur Konvertierung von MP4-Dateien in Audio-Formate."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MP4 zu Audio-Konverter")
        self.setGeometry(300, 300, 400, 250)
        self.setAcceptDrops(True)  # Aktiviert Drag & Drop

        layout = QVBoxLayout()

        # Eingabeordner
        self.input_label = QLabel("Eingabeordner auswählen:")
        layout.addWidget(self.input_label)
        self.input_button = QPushButton("Eingabeordner wählen")
        self.input_button.clicked.connect(self.choose_input_folder)
        layout.addWidget(self.input_button)

        # Zielordner
        self.output_label = QLabel("Zielordner auswählen:")
        layout.addWidget(self.output_label)
        self.output_button = QPushButton("Zielordner wählen")
        self.output_button.clicked.connect(self.choose_output_folder)
        layout.addWidget(self.output_button)

        # Audioformat
        self.format_label = QLabel("Audioformat auswählen:")
        layout.addWidget(self.format_label)

        format_layout = QHBoxLayout()
        self.format_group = QButtonGroup(self)
        format_options = ["mp3", "wav", "", ""]
        self.format_buttons = []

        for format_type in format_options:
            btn = QRadioButton(format_type)
            format_layout.addWidget(btn)  # Hier: Horizontal anordnen
            self.format_group.addButton(btn)
            self.format_buttons.append(btn)

        layout.addLayout(format_layout)
        self.format_buttons[0].setChecked(True)  # Höchste Bitrate als Standard
        button_color = self.styleSheet()
        self.format_buttons[2].setStyleSheet("background-color: transparent;")
        self.format_buttons[3].setStyleSheet("background-color: transparent;")
        self.format_buttons[2].setEnabled(False)  # Deaktivieren
        self.format_buttons[3].setEnabled(False)  # Deaktivieren

        # Bitrate-Optionen nebeneinander
        self.bitrate_label = QLabel("Bitrate auswählen:")
        layout.addWidget(self.bitrate_label)

        bitrate_layout = QHBoxLayout()
        self.bitrate_group = QButtonGroup(self)
        bitrate_options = ["128k", "192k", "256k", "320k"]
        self.bitrate_buttons = []

        for bitrate in bitrate_options:
            btn = QRadioButton(bitrate)
            bitrate_layout.addWidget(btn)  # Hier: Horizontal anordnen
            self.bitrate_group.addButton(btn)
            self.bitrate_buttons.append(btn)

        layout.addLayout(bitrate_layout)
        self.bitrate_buttons[-1].setChecked(True)  # Höchste Bitrate als Standard

        # Samplingrate-Optionen nebeneinander
        self.sampling_label = QLabel("Samplingrate auswählen:")
        layout.addWidget(self.sampling_label)

        sampling_layout = QHBoxLayout()
        self.sampling_group = QButtonGroup(self)
        sampling_options = ["44100", "48000", "", ""]
        self.sampling_buttons = []

        for rate in sampling_options:
            btn = QRadioButton(rate)
            sampling_layout.addWidget(btn)  # Hier: Horizontal anordnen
            self.sampling_group.addButton(btn)
            self.sampling_buttons.append(btn)

        layout.addLayout(sampling_layout)
        self.sampling_buttons[-3].setChecked(True)  # Höchste Samplingrate als Standard
        button_color = self.styleSheet()
        self.sampling_buttons[2].setStyleSheet("background-color: transparent;")
        self.sampling_buttons[3].setStyleSheet("background-color: transparent;")
        self.sampling_buttons[2].setEnabled(False)  # Deaktivieren
        self.sampling_buttons[3].setEnabled(False)  # Deaktivieren

        # Fortschrittsanzeige
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Start-Button
        self.convert_button = QPushButton("Konvertierung starten")
        self.convert_button.clicked.connect(self.convert_videos)
        layout.addWidget(self.convert_button)

        # Abbrechen-Button
        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.cancel_conversion)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        self.input_folder = ""
        self.output_folder = ""

    def choose_input_folder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, "Wähle den Eingabeordner")
        self.input_label.setText(f"{self.input_folder}")

    def choose_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, "Wähle den Zielordner")
        self.output_label.setText(f"{self.output_folder}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.input_folder = os.path.dirname(files[0])  # Ersten Dateiordner als Basis nehmen
        self.input_label.setText(f"{self.input_folder}")

    def convert_videos(self):
        if not self.input_folder or not self.output_folder:
            return

        self.thread = ConverterThread(
            self.input_folder,
            self.output_folder,
            next(btn.text() for btn in self.format_buttons if btn.isChecked()),
            next(btn.text() for btn in self.bitrate_buttons if btn.isChecked()),
            next(btn.text() for btn in self.sampling_buttons if btn.isChecked()),
        )
        self.thread.progress_signal.connect(self.progress_bar.setValue)
        self.thread.start()

    def cancel_conversion(self):
        if hasattr(self, "thread") and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoConverter()
    window.show()
    sys.exit(app.exec())
