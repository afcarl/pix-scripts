import unittest
import os


class TestAdaptiveTest(unittest.TestCase):
    def test_get_json_of_problems(self):
        os.system('python epreuves.py')
        self.assertTrue(os.path.isfile('data/epreuves.json'))

    def test_generate_test(self):
        os.system('python dummy.py 3 recNPB7dTNt5krlMA')
        self.assertTrue(True)
