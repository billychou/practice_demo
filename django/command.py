#!/usr/bin/env python

def find_commands():
    pass


def get_commands():
    commands = { name: 'django.core' for name in find_commands(upath(__path__[0]))}
    if not settings.configured:
        return commands
    for app_config in reversed(list(apps.get_app_config())):
        path = os.path.join(app_config.name, 'management')
        commands.update({name: app_config.name for name in find_commands(path)})
    return commands



class Command(object):



class ManagementUtility(object):
    def __init__(self, argv):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None

    def main_help_text(self, commands_only=False):
        if commands_only:
            usage = sorted(get_commands().keys())



