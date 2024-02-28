from backend.db import db
from backend.config import *

class CustomTextTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(f"Passed: {test}\n")
        
    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(f"rror: {test}\n")
        
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(f"ailed: {test}\n")
        
class CustomTextTestRunner(unittest.TextTestRunner):
    resultclass = CustomTextTestResult

class Tests():
    def run_tests():
        test_suite = unittest.defaultTestLoader.discover(r'backend\\tests', pattern='test_*.py')
        CustomTextTestRunner().run(test_suite)