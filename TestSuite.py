import unittest
from TestUtils import TestUtils


class TestSymbolTable(unittest.TestCase):
    def test_0(self):
        input = ["INSERT a1 number", "INSERT b2 string"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 100))

    def test_1(self):
        input = ["INSERT x number", "INSERT y string", "INSERT x string"]
        expected = ["Redeclared: INSERT x string"]

        self.assertTrue(TestUtils.check(input, expected, 101))

    def test_2(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["TypeMismatch: ASSIGN y 17"]

        self.assertTrue(TestUtils.check(input, expected, 102))

    def test_3(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END",
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 103))

    def test_4(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "1", "0"]

        self.assertTrue(TestUtils.check(input, expected, 104))

    def test_5(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "y//0 x//1 z//1"]

        self.assertTrue(TestUtils.check(input, expected, 105))

    def test_6(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]

        self.assertTrue(TestUtils.check(input, expected, 106))
