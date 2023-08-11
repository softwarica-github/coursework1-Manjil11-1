import unittest
from scanning_function import *
from tkinter import Tk
from dashboard_gui import DashboardInterface  
from scanning_function import ScanningFunction

class TestScanningFunction(unittest.TestCase):

    def setUp(self):
        self.txt_widget = tk.Text()  # Create a Text widget
        self.scanning_function = ScanningFunction(self.txt_widget)  # Pass the Text widget as the argument

    def test_validate_input(self):
        self.assertTrue(self.scanning_function.validate_input('192.168.1.1'))
        self.assertTrue(self.scanning_function.validate_input('http://example.com'))
        self.assertFalse(self.scanning_function.validate_input('invalid_url'))

    def test_is_ip(self):
        self.assertTrue(self.scanning_function.is_ip('192.168.1.1'))
        self.assertFalse(self.scanning_function.is_ip('example.com'))

    def test_prepend_http(self):
        self.assertEqual(self.scanning_function.prepend_http('example.com'), 'http://example.com')
        self.assertEqual(self.scanning_function.prepend_http('http://example.com'), 'http://example.com')

    def test_get_domain_from_url(self):
        self.assertEqual(self.scanning_function.get_domain_from_url('http://example.com/path'), 'example.com')

class EnumerationInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.dashboard = DashboardInterface(self.root)
        self.dashboard.start_enumeration()
        self.enumeration_interface = self.root.winfo_children()[0]
        self.enumeration_interface.txt = tk.Text(self.root)  # Create a Text widget

        self.scanning_function = ScanningFunction(self.enumeration_interface.txt)

    def tearDown(self):
        self.root.destroy()

    def test_validate_input_valid_url(self):
        scanning_function = ScanningFunction(None) 
        self.assertTrue(scanning_function.validate_input('http://example.com'))

    def test_validate_input_invalid_input(self):
        txt_widget = tk.Text()  # Create an instance of tk.Text for 'txt' argument
        scanning_function = ScanningFunction(txt_widget)  # Pass the 'txt' widget to ScanningFunction

if __name__ == '__main__':
    unittest.main()









