#!/usr/bin/python
import os
import logging
import argparse
from gi.repository import Gtk

__author__ = 'lefteris'


def create_argument_parser():
    logger.debug("Parsing Arguments")
    p = argparse.ArgumentParser(description="Desktop Launcher Creator")
    p.add_argument('--name', '-n', help="The application name")
    p.add_argument('--generic-name', '-g',
                   help="The application generic name, if not set the application name will be used")
    p.add_argument('--icon', '-i', help="Absolute path to the application icon")
    p.add_argument('--executable', '-e', help="Absolute path to the application executable")
    p.add_argument('--description', '-d', help="Application description, if not set it will be the application name")
    return p


def print_instructions(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    logger.info("Application launcher created at %s", file_path)
    logger.info("Move it to the appropriate location by issuing: mv %s ~/.local/share/applications", file_path)


def create_launcher(name, generic_name, comment, icon, executable):
    logger.info("Creating desktop launcher")
    if not (name and executable and icon):
        # argument_parser.print_help()
        exit(1)

    if generic_name is None:
        generic_name = name

    if comment is None:
        comment = name

    file_name = name.replace(" ", "-") + ".desktop"
    with open(file_name, "w") as f:
        f.write("[Desktop Entry]\n")
        f.write("Name=%s\n" % name)
        f.write("GenericName=%s\n" % generic_name)
        f.write("Comment=%s\n" % comment)
        f.write("Exec=%s\n" % executable)
        f.write("Icon=%s\n" % icon)
        f.write("Type=Application\n")
        f.write("Name[en_US]=%s\n" % name)
    logger.info("Making %s executable", file_name)
    os.chmod(file_name, 0o755)
    return file_name


def initialize_logger():
    _logger = logging.getLogger("desktop-launcher-creator")
    _logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=formatter)
    _logger.addHandler(stream_handler)
    return _logger


def on_ok_button_clicked(button, event=None):
    logger.info("Ok button clicked")


def on_cancel_button_clicked(button, event=None):
    logger.info("Cancel button clicked")
    Gtk.main_quit()


def on_executable_selected(button, event=None):
    logger.info("Executable selected")


def on_icon_selected(button, event=None):
    logger.info("Icon selected")


def initialize_window():

    handlers = {
        "on_ok_button_clicked": on_ok_button_clicked,
        "on_cancel_button_clicked": on_cancel_button_clicked,
        "on_executable_selected": on_executable_selected,
        "on_icon_selected": on_icon_selected
    }

    builder = Gtk.Builder()
    builder.add_from_file("gui.glade")
    builder.connect_signals(handlers)
    win = builder.get_object("mainWindow")
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    logger = initialize_logger()
    initialize_window()
    # argument_parser = create_argument_parser()
    # arguments = argument_parser.parse_args()
    # print_instructions(create_launcher())
    logger.info("Done")
