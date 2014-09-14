import os
import yaml
import unittest

class TestSuite(unittest.TestCase):
    def runTest(self, path, core):
        for root, dirs, files in os.walk(path):
            self._curent_test = ''.join(root.split('/')[-1])
            files_path = ['/'.join([root,file_name]) for file_name in files]
            result = core(self._prepare(files_path), self._curent_test)

            if result:
                self.assertEqual(*result)

    def _prepare(self, files_path):
        data = {}

        for path in files_path:
            name_in_dict = ''.join(path.split('/')[-1]).replace('.json', '')
            with open(path) as f:
                data[name_in_dict] = yaml.load(f)
        
        return data
