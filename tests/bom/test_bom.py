import pathlib
import os
from unittest import TestCase
from unittest.mock import patch
from typing import List
from mdbom.bom.bom import Package, Processor, ProcessingError


class DefaultProcessor(Processor):
    def __init__(self, name=""):
        super(DefaultProcessor, self).__init__(processor_name=name)

    def construct_urls(self, packages: List[Package]) -> List[Package]:
        for package in packages:
            package.url = "https://test.com"

        return packages


class TestProcessor(TestCase):

    input_dir = pathlib.Path.cwd() / "tests" / "inputs"

    def test_create_processor_fails_due_to_empty_name(self):
        with self.assertRaises(ProcessingError) as pe:
            proc = DefaultProcessor()
        self.assertEqual("No processor name defined", str(pe.exception))

    def test_create_processor_success(self):
        proc = DefaultProcessor(name="Default")
        self.assertEqual("Default", proc.processor_name)

    def test_load_bom_fails_due_to_empty_file_name(self):
        proc = DefaultProcessor(name="Default")
        with self.assertRaises(ProcessingError) as pe:
            proc._load_bom()
        self.assertEqual("No file provided", str(pe.exception))

    @patch("os.path.exists")
    def test_load_bom_fails_due_to_file_does_not_exist(self, path_patch):
        proc = DefaultProcessor(name="Default")
        path_patch.return_value = False
        with self.assertRaises(ProcessingError) as pe:
            proc._load_bom(filename="bom.json")
        self.assertEqual("Provided file does not exist", str(pe.exception))

    def test_load_bom_success(self):
        proc = DefaultProcessor(name="Default")
        packages = proc._load_bom(filename=self.input_dir / "bom.json")
        self.assertEqual("argcomplete", packages["components"][0]["name"])
