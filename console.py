#!/usr/bin/python3


"""
Console For AirBnb Clone
"""
import cmd
import json
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User


class HBNBCommand(cmd.Cmd):
    """attribute to display text"""
    prompt = "(hbnb) "
    jfile = 'file.json'
    l_classes = {
            'BaseModel': BaseModel
            #'User': User
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
            class_object = HBNBCommand.l_classes[arg]
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

    def do_destroy(self, arg):
        """deletes an string representation
        of an intance based on the class name and id
        """

        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.l.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for key, value in all_objs.items():
                obj_name = value.__class__.__name__
                obj_id = value.id
                if obj_name == arg[0] and obj_id == args[1].strip('"'):
                    del value
                    del storage.__FileStorage__objects[key]
                    storage.save()
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

        if args[0] not in HBNBCommand.l_classes:
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

    def do_update(self, arg):
        arg1 = split('')
        """function is used to split and store the arguments"""
        obj_dict1 = storage.all()

        if len(arg) == 0:
            print("** class name missing **")
            return False
        if arg1[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
            return False
        if len(arg1) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg1[0], arg[1]) not in obj_dict1.keys():
            print("** no instance found **")
            return False
        if len(arg1) == 2:
            print("** attribute name missing **")
            return False
        if len(arg1) > 3:
            value = arg1[3]
        else:
            print("** value missing **")
            return False
        if len(arg1) == 4:
            """updating the instance"""
            obj = obj_dict1["{}.{}".format(arg1[0], arg1[1])]
            if arg1[2] in obj.__class__.dict__.keys():
                val_type = type(obj.__class__.__dict__[arg1[2]])
                obj.__dict__[arg1[2]] = val_type(arg1[3])
            else:
                obj.__dict__[arg1[2]] = arg1[3]
        elif type(eval(arg1[2])) == dict:
            obj = obj_dict1["{}.{}".format(arg1[0], arg1[1])]
            for key1, value1 in eval(arg1[2]).items():
                if (key1 in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key1]) in
                        {str, int, float}):
                    val_type = type(obj.__class__.__dict__[key1])
                    obj.__dict__[key1] = val_type(value1)
                else:
                    obj.__dict__[key1] = val_type(value1)
        storage.save() 
        return split(arg)

    def do_quit(self, line):
        """commmand to exit program"""
        return True

    def do_EOF(self, line):
        """Exit the program"""
        return True

    def emptyline(self):
        """
        Do nothing when an empty line is entered
        """
        pass

"""ensures that the code runs
only when console.py file is run""" 
if __name__ == '__main__':
    HBNBCommand().cmdloop()
