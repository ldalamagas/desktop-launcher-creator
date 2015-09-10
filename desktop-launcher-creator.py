#!/usr/bin/python
import os
import logging
import argparse

__author__ = 'lefteris'


def create_argument_parser():
    p = argparse.ArgumentParser(description="Desktop Launcher Creator")
    p.add_argument('--gui', "-g", dest="gui",  help="Enable graphical user interface", action="store_true")
    p.add_argument('--name', '-n', help="The application name")
    p.add_argument('--generic-name', help="The application generic name, if not set the application name will be used")
    p.add_argument('--icon', '-i', help="Absolute path to the application icon")
    p.add_argument('--executable', '-e', help="Absolute path to the application executable")
    p.add_argument('--comment', '-c', help="Application description, if not set it will be the application name")
    p.add_argument('--debug',  help="Enable debugging features", action="store_true")
    p.set_defaults(gui=False)
    return p


def print_instructions(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    logger.info("Application launcher created at %s", file_path)
    logger.info("Move it to the appropriate location by issuing: mv %s ~/.local/share/applications", file_path)


def create_launcher(name, generic_name, comment, icon, executable):
    if not (name and executable and icon):
        argument_parser.print_help()
        exit(1)

    logger.debug("Creating desktop launcher")

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

    if arguments.debug:
        _logger.setLevel(logging.DEBUG)
    else:
        _logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(levelname)s: %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=formatter)
    _logger.addHandler(stream_handler)
    return _logger


def on_ok_button_clicked(_):
    logger.debug("Ok button clicked")
    create_launcher(
        gui_objects["name"].get_text(),
        gui_objects["generic_name"].get_text(),
        gui_objects["comment"].get_text(),
        gui_objects["icon"].get_filename(),
        gui_objects["executable"].get_filename())


def on_cancel_button_clicked(_, event=None):
    _ = event   # Avoid IDE warning
    logger.debug("Cancel button clicked")
    Gtk.main_quit()


def on_executable_selected(_):
    logger.debug("Executable selected")


def on_icon_selected(_):
    logger.debug("Icon selected")


def initialize_gui():

    handlers = {
        "on_ok_button_clicked": on_ok_button_clicked,
        "on_cancel_button_clicked": on_cancel_button_clicked,
        "on_executable_selected": on_executable_selected,
        "on_icon_selected": on_icon_selected
    }

    builder = Gtk.Builder()
    builder.add_from_file("gui.glade")
    builder.connect_signals(handlers)

    # Retrieve all the gui objects in a dictionary
    go = {
        "window": builder.get_object("mainWindow"),
        "name": builder.get_object("txtName"),
        "generic_name": builder.get_object("txtGenericName"),
        "comment": builder.get_object("txtComment"),
        "executable": builder.get_object("fcExecutable"),
        "icon": builder.get_object("fcIcon")
    }
    return go

if __name__ == "__main__":
    argument_parser = create_argument_parser()
    arguments = argument_parser.parse_args()
    logger = initialize_logger()
    if arguments.gui:
        from gi.repository import Gtk
        logger.debug("Graphical user interface enabled")
        gui_objects = initialize_gui()
        gui_objects["window"].show_all()
        Gtk.main()
    else:
        txt_name = None
        txt_generic_name = None
        txt_comment = None
        fc_executable = None
        fc_icon = None
        logger.debug("Command line interface enabled")
        print_instructions(create_launcher(arguments.name, arguments.generic_name,
                                           arguments.comment, arguments.icon, arguments.executable))
    logger.debug("Done")
