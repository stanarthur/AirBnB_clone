#!/usr/bin/env python3

"""
This module contains several unittest test cases of the console of class
HBNBCommand. The tests are done by intersecting the stdout, redirecting
the stdout using patch function from unittest.mock module, to a file
object using StringIO.

"""

import os
import unittest
import pep8
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):
    """Test the console program by intersecting the stdout"""

    def test_pep8(self):
        """Test code conformity to pep8 style"""
        style = pep8.StyleGuide()
        num_err = 0
        files = ["console.py", "tests/test_console.py"]
        num_err += style.check_files(files).total_errors
        self.assertEqual(num_err, 0, "Wrong pep8 format, adjust your code !")

    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_quit(self):
        """Test quit"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            output = f.getvalue().strip()
            self.assertFalse(output)

    def test_EOF(self):
        """Test end of file or ctrl-d"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            output = f.getvalue().strip()
            self.assertFalse(output)

    def test_empty_line(self):
        """Test when no command is inputed in command prompt"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
            output = f.getvalue().strip()
            self.assertEqual(output, "")

    def test_create(self):
        """Test create new oject"""
        with patch('sys.stdout', new=StringIO()) as f:
            """missing class name"""
            HBNBCommand().onecmd("create")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            """valid class name"""
            HBNBCommand().onecmd("create User")
            output1 = f.getvalue().strip()
            self.assertTrue(isinstance(output1, str))
            self.assertTrue(len(output1) > 5)

        with patch('sys.stdout', new=StringIO()) as f:
            """check output"""
            HBNBCommand().onecmd("all")
            output_1 = f.getvalue()[:8]
            self.assertEqual(output_1, '["[User]')

        with patch('sys.stdout', new=StringIO()) as f:
            """Invalid class name"""
            HBNBCommand().onecmd("create Mymodel")
            output2 = f.getvalue().strip()
            self.assertEqual(output2, "** class doesn't exists **")

    def test_show(self):
        """Test instance in string"""
        with patch('sys.stdout', new=StringIO()) as f:
            """missing class name"""
            HBNBCommand().onecmd("show")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            """missing id """
            HBNBCommand().onecmd("show User")
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            """invalid class"""
            HBNBCommand().onecmd("Mymodel.show()")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            """non-existing instance id"""
            HBNBCommand().onecmd("User.show('121212')")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_destroy(self):
        """Test destroying of instances based on id"""

        with patch('sys.stdout', new=StringIO()) as f:
            """missing class name"""
            HBNBCommand().onecmd("destroy")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            """missing id """
            HBNBCommand().onecmd("destroy User")
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            """invalid class"""
            HBNBCommand().onecmd("Mymodel.destroy()")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            """non-existing instance id"""
            HBNBCommand().onecmd("User.destroy('121212')")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_all(self):
        """Test all instances in an array"""

        with patch('sys.stdout', new=StringIO()) as f:
            """all instances"""
            HBNBCommand().onecmd("all")
            output = f.getvalue().strip()
            self.assertEqual(output, "[]")
            self.assertTrue(isinstance(output, str))

        with patch('sys.stdout', new=StringIO()) as f:
            """non-existing instances"""
            HBNBCommand().onecmd("all Mymodel")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            """create instances """
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("create Review")

        with patch('sys.stdout', new=StringIO()) as f:
            """Check specific instances"""
            HBNBCommand().onecmd("all User")
            output = f.getvalue().strip()[:8]
            self.assertEqual(output, '["[User]')

        with patch('sys.stdout', new=StringIO()) as f:
            """Check specific instances"""
            HBNBCommand().onecmd("all Review")
            output = f.getvalue().strip()[:10]
            self.assertEqual(output, '["[Review]')

    def test_count(self):
        """Test number of a particular instane"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count MyModel")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count User")
            output = f.getvalue().strip()
            self.assertEqual(output, '1')

        with patch('sys.stdout', new=StringIO()) as f:
            """create instances"""
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("create Review")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count User")
            output = f.getvalue().strip()
            self.assertEqual(output, '2')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Review.count()")
            output = f.getvalue().strip()
            self.assertEqual(output, '2')

    def test_update(self):
        """Test updated instances"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

if __name__ == "__main__":
    unittest.main()
