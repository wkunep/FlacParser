import sys
import argparse

try:
    from PyQt5.QtWidgets import QApplication
except ImportError as exception:
    sys.exit("PyQt5 not found {}".format(exception))

try:
    from pattern import Pattern
    from flacExtractor import FlacParser
    from gui import Window
except ImportError as exception:
    sys.exit("Some program module not found: {}".format(exception))


def get_arguments():
    parser = argparse.ArgumentParser(description='''The programm for parsing flac files.
    input file name is entered with extension .flac and
    output file name with extension .txt
    To run graphic version use: -g or --gui
    ''')
    parser.add_argument('--file_name', '-f', dest='file_name',
                        help='input file name *.flac', required=True)
    parser.add_argument('--output_file_name', '-o', dest='output',
                        default='output.html',
                        help='output file name *.txt default output.txt')
    parser.add_argument('--gui', '-g', action='store_true',
                        help='enable gui')
    args = parser.parse_args()
    return args


def graphical_version(flac_file, output):
    app = QApplication(sys.argv)
    window = Window(flac_file, output)
    sys.exit(app.exec_())


def console_version(flac_file, output):
    try:
        with open(flac_file, 'rb') as f:
            data = f.read()
    except Exception as exception:
        sys.exit("Error! {}".format(exception))
    pattern = Pattern(flac_file, output)

    flac_parser = FlacParser(data, pattern)
    flac_parser.parse()

    pattern.write()


def main():
    arguments = get_arguments()
    flac_file = arguments.file_name
    output = arguments.output

    if arguments.gui:
        graphical_version(flac_file, output)
    else:
        console_version(flac_file, output)


if __name__ == "__main__":
    main()
