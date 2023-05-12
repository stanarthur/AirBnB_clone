#!/usr/bin/python3

import cmd

class HBNBCommand(cmd.Cmd):

    """attribute to display text"""
    prompt = "(hbnb) "

    """command to exit the program"""
    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        """Exit the program"""
        return True

"""ensures that the code runs
only when console.py file is run""" 
if __name__ == '__main__':
    HBNBCommand().cmdloop()
