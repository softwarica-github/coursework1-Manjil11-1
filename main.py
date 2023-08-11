import tkinter as tk
import unittest
from enumeration_gui import EnumerationInterface
from dashboard_gui import DashboardInterface
from scanning_function import ScanningFunction
from unit_test import  TestScanningFunction,EnumerationInterfaceTests

def main():

    # Create the test suite
    test_suite = unittest.TestSuite()

    # Add the test cases to the test suite
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestScanningFunction))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EnumerationInterfaceTests))

    # Run the tests
    unittest.TextTestRunner().run(test_suite)




if __name__ == '__main__':
    # Run the unit tests first
    root = tk.Tk()
    root.geometry("800x600")
    dashboard = DashboardInterface(root)
    root.mainloop()
    main()



