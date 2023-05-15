#!/usr/bin/python3
"""
Console For AirBnb Clone
"""
import cmd
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
            obj_dict = storage.all()
            """retrives all the objects stored in storage instance"""

            for key, value in obj_dict.items():
                obj_name = value.__class__.__name__
                """retrieves the name of the class of the object
                'value'
                """
                obj_id = value.id
                if obj_name == args[0] and obj_id == args[1].strip('"'):
                    print(value)
                    return
            print("** no instance found **")

    def do_destroy(self, arg):
        """deletes an string representation
        of an intance based on the class name and id
        """

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')
        obj_dict = storage.all()

        if args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            instance_key = "{}>{}".format(args[0], args[1])
            if instance_key not in obj_dict.keys():
                print("** no instance found **")
            return

    def do_all(self, arg):
        """ Prints string represention of all instances
        of a given class
        """

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')
        obj_dict = storage.all()

        if len(args) > 0 and args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
        else:
            list_instances = []
            for key, value in obj_dict.items():
                obj_name = value.__class__.__name__
                if obj_name == args[0]:
                    list_instances += [value.__str__()]
                    """adds to string representation of an object
                    to the 'list_instance' list
                    """
            print(list_instances)

    def do_update(self, arg):
        """Function used to update the instance of a class"""
        args = split(arg)
        obj_dict = storage.all()

        if len(arg) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                value = eval(args[2])
                if isinstance(value, dict):
                    print("** value missing **")
                    return False
            except NameError:
                print("** value missing **")
                return False
            
        """updating the instance"""
        if len(args) == 4:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                v_type = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = v_type(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            for k, v in eval(args[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    v_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = v_type(v)
                else:
                    obj.__dict__[k] = v
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
