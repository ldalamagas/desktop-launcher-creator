#!/usr/bin/python
import os
import logging
import argparse

__author__ = 'lefteris'


def create_argument_parser():
    logger.debug("Parsing Arguments")
    p = argparse.ArgumentParser(description="Desktop Launcher Creator")
    p.add_argument('--name', '-n', help="The application name")
    p.add_argument('--generic-name', '-g', help="The application generic name, if not set the application name will be used")
    p.add_argument('--icon', '-i', help="Absolute path to the application icon")
    p.add_argument('--executable', '-e', help="Absolute path to the application executable")
    p.add_argument('--description', '-d', help="Application description, if not set it will be the application name")
    return p


def print_instructions(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    logger.info("Application launcher created at %s", file_path)
    logger.info("Move it to the appropriate location by issuing: mv %s ~/.local/share/applications", file_path)


def create_launcher():
    logger.info("Creating desktop launcher")
    if not (arguments.name and arguments.executable and arguments.icon):
        argument_parser.print_help()
        exit(1)

    if arguments.generic_name is None:
        arguments.generic_name = arguments.name

    if arguments.description is None:
        arguments.description = arguments.name

    file_name = arguments.name.replace(" ", "-") + ".desktop"
    with open(file_name, "w") as f:
        f.write("[Desktop Entry]\n")
        f.write("Name=%s\n" % arguments.name)
        f.write("GenericName=%s\n" % arguments.generic_name)
        f.write("Exec=%s\n" % arguments.executable)
        f.write("Icon=%s\n" % arguments.icon)
        f.write("Type=Application\n")
        f.write("Name[en_US]=%s\n" % arguments.name)
    logger.info("Making %s executable", file_name)
    os.chmod(file_name, 0755)
    return file_name


if __name__ == "__main__":
    logger = logging.getLogger("desktop-launcher-creator")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=formatter)
    logger.addHandler(stream_handler)
    argument_parser = create_argument_parser()
    arguments = argument_parser.parse_args()
    print_instructions(create_launcher())
    logger.info("Done")