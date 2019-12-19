from unittest import TestLoader, TestSuite
from unittest import TextTestRunner

tests = TestSuite()

for dir_ in ['./', './database/']:
    loader = TestLoader()
    test = loader.discover(dir_, pattern='*Test.py')
    tests.addTest(test)

runner = TextTestRunner(verbosity=2)
runner.run(tests)
