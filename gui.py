import sys

try:
    import pyglet
except ImportError as exception:
    IS_PYGLET_IMPORT = False
try:
    from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, \
        QApplication, QSlider, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
        QLineEdit, QWidget
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QIcon
except ImportError as exception:
    sys.exit("PyQt5 not found {}".format(exception))

try:
    from pattern import Pattern
    from flacExtractor import FlacParser
except ImportError as exception:
    sys.exit("Some program module not found: {}".format(exception))

IS_PYGLET_IMPORT = True


class Window(QMainWindow):
    def __init__(self, flac_file, output):
        self.flac_file = flac_file
        self.output = output
        if IS_PYGLET_IMPORT:
            self.player = pyglet.media.Player()
            self.player.queue(pyglet.resource.media(flac_file))
            self.player.volume = 0

        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar()

        workspace = QWidget()
        self.setCentralWidget(workspace)

        text = QLabel("Parsing File")
        self.text_edit = QTextEdit()

        sound_volume_label = QLabel("Sound Volume")
        sound_volume_slider = QSlider(Qt.Horizontal, self)
        sound_volume_slider.setFocusPolicy(Qt.NoFocus)
        sound_volume_slider.valueChanged[int].connect(self.change_volume_value)

        grid = QGridLayout(workspace)
        grid.setSpacing(10)
        grid.addWidget(sound_volume_label, 2, 0)
        grid.addWidget(sound_volume_slider, 2, 1)
        grid.addWidget(text, 3, 0)
        grid.addWidget(self.text_edit, 3, 1, 5, 1)

        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction(self.create_open_file_action())
        file_menu.addAction(self.create_parse_file_action())
        file_menu.addAction(self.create_play_file_action())
        file_menu.addAction(self.create_pause_file_action())
        file_menu.addAction(self.create_exit_action())

        self.setGeometry(300, 100, 800, 600)
        self.setWindowTitle('Flac')
        self.show()

    def create_open_file_action(self):
        open_file_action = QAction('&Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.setStatusTip('Open new File')
        open_file_action.triggered.connect(self.open_file)
        return open_file_action

    def create_parse_file_action(self):
        parse_file_action = QAction('&Parse', self)
        parse_file_action.setShortcut('Ctrl+P')
        parse_file_action.setStatusTip('Parse current file')
        parse_file_action.triggered.connect(self.parse_file)
        return parse_file_action

    def create_play_file_action(self):
        play_file_action = QAction('&Play', self)
        play_file_action.setStatusTip('Play current file')
        play_file_action.triggered.connect(self.play_file)
        return play_file_action

    def create_pause_file_action(self):
        pause_player_action = QAction('&Pause', self)
        pause_player_action.setStatusTip('Pause play current file')
        pause_player_action.triggered.connect(self.pause_play)
        return pause_player_action

    def create_exit_action(self):
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close_gui)
        return exit_action

    def change_volume_value(self, value):
        if IS_PYGLET_IMPORT:
            self.player.volume = value / 100

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if file_name:
            self.flac_file = file_name
            if IS_PYGLET_IMPORT:
                if self.player.playing:
                    self.player.pause()
                self.player.delete()
                self.player.queue(pyglet.media.load(self.flac_file))

    def parse_file(self):
        try:
            with open(self.flac_file, 'rb') as f:
                data = f.read()
        except Exception as exception:
            sys.exit("Error! {}".format(exception))
        pattern = Pattern(self.flac_file, self.output)
        flac_parser = FlacParser(data, pattern)
        flac_parser.parse()
        pattern.write()
        self.text_edit.setText(pattern.get_output_string())

    def play_file(self):
        if IS_PYGLET_IMPORT:
            if not self.player.playing:
                self.player.play()
                pyglet.app.run()
        else:
            print("Need pyglet and AVbin from to play file")
            sys.exit("Need pyglet and AVbin from to play file")

    def pause_play(self):
        if IS_PYGLET_IMPORT:
            self.player.pause()

    def close_gui(self):
        if IS_PYGLET_IMPORT:
            self.player = None
            pyglet.app.exit()
        self.close()
