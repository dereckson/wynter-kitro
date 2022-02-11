#!/usr/bin/env python3

import os
import sys
import yaml


#   -------------------------------------------------------------
#   Configuration file
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_configuration_file_path_candidates():
    candidates = [
        "/usr/local/etc/organize/folders.yml",
        "/etc/organize/folders.yml",
    ]

    try:
        candidates.append(os.environ["HOME"] + "/.config/organize/folders.yml")
    except KeyError:
        pass

    return candidates


def get_configuration_file_path():
    for file_path in get_configuration_file_path_candidates():
        if os.path.exists(file_path):
            return file_path

    raise Exception("Can't find configuration file.")


#   -------------------------------------------------------------
#   Folders organizer
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Organizer(object):

    def __init__(self):
        self.configuration_file_path = get_configuration_file_path()
        self.folders = self.read_folders()

    def read_folders(self):
        folders = yaml.safe_load(open(self.configuration_file_path))

        if folders is None:
            return {}

        return folders

    def get(self, folderType):
        return self.folders[folderType]

    def set(self, folderType, folderPath):
        self.folders[folderType] = folderPath

    def save(self):
        fd = open(self.configuration_file_path, "w")
        print(yaml.dump(self.folders), file=fd)
        fd.close()


#   -------------------------------------------------------------
#   Folders organizer command
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class OrganizerCommand(object):

    def __init__(self, organizer):
        self.organizer = organizer

    def get(self, folderType):
        try:
            folder = self.organizer.get(folderType)
        except KeyError:
            return False

        print(folder)

        return True

    def set(self, folderType, folderPath):
        self.organizer.set(folderType, folderPath)
        self.organizer.save()

        return True


#   -------------------------------------------------------------
#   Helpers
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def s(count):
    if count > 1:
        return "s"

    return ""


#   -------------------------------------------------------------
#   Run task
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def run(command, args):
    organizer = Organizer()
    organiserCommand = OrganizerCommand(organizer)

    # Calls organizer.{command}({args})

    try:
        method = getattr(organiserCommand, command)
    except AttributeError:
        print("Command not found:", command, file=sys.stderr)
        exit(2)

    expectedArgsCount = method.__code__.co_argcount - 1
    if len(args) != expectedArgsCount:
        print("Command", command, "expects", expectedArgsCount,
              "argument." + s(expectedArgsCount))
        exit(4)

    result = method(*args)

    exitCode = 0 if result else 1
    sys.exit(exitCode)


if __name__ == "__main__":
    argc = len(sys.argv)

    if argc < 2:
        print("Usage: organize-folders <command> [arguments]", file=sys.stderr)
        exit(8)

    run(sys.argv[1], sys.argv[2:])
