#!/usr/bin/python3
"""
Console For AirBnb Clone
"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """This class contains the entry point of the command interpreter
    Attributes:
        Fields:
            prompt: Customize the command interpreter prompt
        Methods:
            do_quit(self, line): Quit the cosole using "quit" command
            do_EOF(self, line): Quit the console using "CTRL-D" keyboard
            emptyline(self): Disable repitition of last/previous command
            do_create(self, line): Create new instance of specified class
            do_show(self, line): Display instances using class and ID
            do_destroy(self, line): Destroy an instance using it's class and ID
            do_all(self, line): List all instances based on specified class/not
            do_update(self, line): Update an instance by adding more attributes
            through dictionary or by specifying the attribute name value pair
    """
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
            return

        args = arg.split()
        if args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
            return
        else:
            my_model = eval(args[0])()
            """creating a new instance"""
            print(my_model.id)
            my_model.save()

    def do_show(self, arg):
        """prints string representatation
        of an instance
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()

        if args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        else:
            try:
                key = "{}.{}".format(args[0], args[1])
                if key in storage.all():
                    """retrives all the objects stored in storage instance"""
                    print(storage.all()[key])
                else:
                    print("** no instance found **")
                    return
            except Exception:
                return

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
            return
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            try:
                instance_key = "{}.{}".format(args[0], args[1])
                del storage.all()[instance_key]
                storage.save()
                storage.reload()
            except Exception:
                print("** no instance found **")
            return

    def do_all(self, arg):
        """ Prints string represention of all instances
        of a given class
        """

        objects = []
        response = "** class doesn't exist **"
        if not arg:
            [objects.append(str(i)) for i in storage.all().values()]
        else:
            if arg not in HBNBCommand.l_classes:
                print(response)
                return
            else:
                [
                        objects.append(str(i)) for i in storage.all().values()
                        if i.__class__.__name__ == arg]
                print(objects)

    def do_count(self, arg):
        """Function used to count number of instances present"""
        if arg not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
            return
        else:
            num = sum(
                    1 for i in storage.all().values()
                    if i.__class__.__name__ == arg)
            print(num)


    def do_update(self, arg):
        """Function used to update the instance of a class"""
        args = split(arg)
        obj_dict = storage.all()

        if not arg:
            print("** class name missing **")
            return
        pattern = r'({.*?})|(\".*?\")'
        txt_in_braces = re.findall(pattern, arg)

        """Replace spaces in the list above with # and
        join them with the line"""
        for space in txt_in_braces:
            space_str = "".join(space)
            arg = arg.replace(space_str, space_str.replace(' ', '###'))
         
            """Split the arg using space and replace ### in
        {} and "" back with spaces"""
        args = [a.replace('###', ' ') for a in arg.split()]
        
        if args[0] not in HBNBCommand.l_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            key ="{}.{}".format(args[0], args[1].strip('"').strip('"'))
            if key not in storage.all():
                print("** no instance found **")
                return
            else:
                print("** attribute name missing **")
                return

        elif len(args) == 3:
                    if args[2].startwith('{'):
                        if commands[2].endswith('}'):
                            data_dict= eval(args[2])
                            key = "{}.{}".format(args[0], args[1].strip('"').strip("'"))
                            update_obj = storage.all()[key]
                            for i, j in data_dict.items():
                                setattr(update_obj, i, j)
                            update.obj.save()
                        else:
                            print("** Invalid syntax **")
                            return
                    else:
                        print("** value missing **")
                        return
            
        """updating the instance"""
        if len(args) == 4:
            val = args[3]
            if type(eval(val)) not in (float, int, dict):
                val = str(val).strip('"').strip("'")
            else:
                val = eval(val)
            key = "{}.{}".format(args[0], args[1].strip('"').strip("'"))
            if key in storage.all():
                update_obj = storage.all()[key]
                cmd_key = args[2].strip("'").strip('"')
                setattr(update_obj, cmd_key, val)
                update_obj.save()
            else:
                print("** no instance found **")
                return
        else:
            print("** Invalid syntax **")
            return
    
    def get_list_of_args(self, command):
        obj_id = ""
        attr = ""
        new_val = ""
        className = ""
        functionName = ""
        try:
            core_args = command.split("(")[0].split(".")
            """User.update"""
            all_args = command.split("(")[1][:-1]
            """*args + **kwargs"""
            className = core_args[0]
            functionName = core_args[1]
            if all_args != "":
                first_brace, second_brace = self.check_for_braces(all_args,
                                                                  "{", "}")
                if first_brace is not False:
                    arguments = all_args[:first_brace - 2]
                else:
                    arguments = all_args
                """eliminate any white space"""
                arguments = ' '.join(arguments.split())
                arguments = arguments.split(maxsplit=2, sep=",")
                obj_id = arguments[0].strip("\" ")
                attr = arguments[1].strip("\" ")
                try:
                    index_brace = arguments[2].index("]")  # if we found "["
                    new_val = arguments[2][:index_brace + 1].strip("\" ")
                except Exception:
                    new_val = arguments[2]  # if we didn't found "["
            return className, functionName, obj_id, attr, new_val
        except Exception as ex:
            # print(ex)
            return className, functionName, obj_id, attr, new_val

    
    def default(self, line):
        """
            Change Default console action:
            Usage:
                <class name>.count()
                <class name>.all()
                <class name>.show(<id>)
                <class name>.destroy(<id>)
                <class name>.update(<id>, <attribute name>, <attribute value>)
        """
        first_brace, second_brace = self.check_for_braces(line, "{", "}")
        if first_brace is not False:
            core_string = line[:first_brace]
            str_dict = line[first_brace: second_brace + 1]
            dict_args = eval(str_dict)
            for key, val in dict_args.items():
                command = core_string + repr(key) + ', ' + repr(val) + ')'
                self.default(command)
            return
        try:
            args = self.get_list_of_args(line)

            if len(args) > 1:
                className, functionName, obj_id, attr, new_val = args
                if inspect.isclass(eval(className)) is True:
                    arg = className + ' ' + obj_id
                    if functionName == "all":
                        return self.do_all(className)
                    elif functionName == "show":
                        return self.do_show(arg)
                    elif functionName == "destroy":
                        return self.do_destroy(arg)
                    elif functionName == "update":
                        return self.do_update(arg + ' ' + attr + ' ' + new_val)
                    elif functionName == "count":
                        i = 0
                        object_container = storage.all()
                        for obj_id, obj in object_container.items():
                            if type(obj) is eval(className):
                                i += 1
                        print(i)
            else:
                print("*** Unknown syntax: {}".format(line))
                return False
        except Exception:
            pass


    def do_quit(self, line):
        """commmand to exit program"""
        return True

    def do_EOF(self, line):
        """Exit the program"""
        print()
        return True

    def emptyline(self, line):
        """Do nothing upon receiving an empty line."""
        pass

        """ensures that the code runs
        only when console.py file is run"""
if __name__ == '__main__':
    HBNBCommand().cmdloop()
