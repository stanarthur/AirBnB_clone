#!/usr/bin/python3
"""
Console For AirBnb Clone
"""
import re
import cmd
import json
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """attribute to display text"""
    prompt = "(hbnb) "
    jfile = 'file.json'
    l_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def do_create(self, arg):
        """creates,save and prints
        the id an instance of BaseModel
        """
        if not arg:
            print("** class name missing **")
        elif arg not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
        else:
            class_object = eval(arg)
            """creating a new instance"""
            my_model = class_object()
            print(my_model.id)
            my_model.save()

    def do_show(self, arg):
        """prints string representatation
        of an instance
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            """retrives all the objects stored in storage instance"""

            for key, value in all_objs.items():
                obj_name = value.__class__.__name__
                """retrieves the name of the class of the object
                'value'
                """
                obj_id = value.id
                if obj_name == args[0] and obj_id == args[1].strip('"'):
                    print(value)
                    return
            print("** no instance found **")

    def do_all(self, arg):
        """ Prints string represention of all instances
        of a given class 
        """

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if len(args) > 0 and args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
        else:
            all_objs = storage.all()
            list_instances = []
            for key, value in all_objs.items():
                obj_name = value.__class__.__name__
                if obj_name == args[0]:
                    list_instances += [value.__str__()]
                    """adds to string representation of an object
                    to the 'list_instance' list
                    """
            print(list_instances)

    def do_destroy(self, arg):
        """deletes an instance based on the class name and id"""

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return

        objs = storage.all()
        obj_key = args[0] + '.' + args[1]
        if obj_key in objs:
            del objs[obj_key]
            storage.save()
        else:
            print("** no instance found **")
    
    def do_update(self, arg):
        """updates an instance based on the class name and id"""

        if not arg:
            print("** class name missing **")
            return

        args = split(arg)
        if args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return

        objs = storage.all()
        obj_key = args[0] + '.' + args[1]
        if obj_key not in objs:
            print("** no instance found **")
            return

        obj = objs[obj_key]
        attr_dict = obj.to_dict()
        if len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return

        attr_name, attr_value = args[2], args[3]
        if attr_name not in attr_dict:
            obj.__setattr__(attr_name, attr_value)
            storage.save()
        else:
            attr_type = type(attr_dict[attr_name])
            try:
                attr_value = attr_type(attr_value)
            except ValueError:
                pass
            obj.__setattr__(attr_name, attr_value)
            storage.save()
    
    def default(self, arg):
        """Default behaviour for cmd module when input is invalid"""
        argdict = {
            "create": self.do_create,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "all": self.do_all,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False



    def do_quit(self, line):
        """commmand to exit program"""
        return True

    def do_EOF(self, line):
        """Exit the program"""
        return True

    def emptyline(self, line):
        """Do nothing upon receiving an empty line."""
        pass

"""ensures that the code runs
only when console.py file is run""" 
if __name__ == '__main__':
    HBNBCommand().cmdloop()

