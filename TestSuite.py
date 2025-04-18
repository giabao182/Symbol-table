import unittest
from TestUtils import TestUtils


from SymbolTable import *


class TestSymbolTable(unittest.TestCase):
    def test_0(self):
        input = ["INSERT a1 number", "INSERT b2 string"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 100))

    def test_1(self):
        input = ["INSERT x number", "INSERT y string", "INSERT x string"]
        expected = ["success", "success", "Redeclared: INSERT x string"]

        self.assertTrue(TestUtils.check(input, expected, 101))

    def test_2(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["success", "success", "success", "TypeMismatch: ASSIGN y 17", "TypeMismatch: ASSIGN x 'abc'"]

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

    def test_7(self):
        input = [
            "ASSIGN x 4"
        ]
        expected = ["Undeclared: ASSIGN x 4"]
        self.assertTrue(TestUtils.check(input, expected, 107))
    def test_8(self):
        input = [
            "INSERT a number",
            "INSERT b string",
            "BEGIN",
            "INSERT a string",  # shadowing
            "INSERT c number",
            "PRINT",
            "END",
            "PRINT"
        ]
        expected = [
            "success", "success", "Redeclared: INSERT a string", "success", "a//0 b//0 c//1", "a//0 b//0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 108))
    def test_9(self):
        input = [
            "INSERT a number",
            "INSERT b string",
            "ASSIGN a 42",
            "ASSIGN b 'hello'",
            "ASSIGN b 42",
            "ASSIGN a 'wrong'"
        ]
        expected = [
            "success", "success", "success", "success",
            "TypeMismatch: ASSIGN b 42", "TypeMismatch: ASSIGN a 'wrong'"
        ]
        self.assertTrue(TestUtils.check(input, expected, 109))
    def test_10(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "INSERT b string",
            "BEGIN",
            "INSERT c number",
            "LOOKUP a",
            "LOOKUP b",
            "LOOKUP c",
            "END",
            "LOOKUP c",
            "END",
            "LOOKUP b"
        ]
        expected = [
            "success", "success", "success", "0", "1", "2", "Undeclared: LOOKUP c", "Undeclared: LOOKUP b"
        ]
        self.assertTrue(TestUtils.check(input, expected, 110))
    def test_11(self):
        input = [
            "END"
        ]
        expected = [
            "UnknownBlock"
        ]
        self.assertTrue(TestUtils.check(input, expected, 111))
    def test_12(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT x string",
            "INSERT y number",
            "BEGIN",
            "INSERT z string",
            "PRINT",
            "BEGIN"
        ]
        expected = [
            "success", "Redeclared: INSERT x string", "success", "success", "x//0 y//1 z//2", "UnclosedBlock: 3"
        ]
        self.assertTrue(TestUtils.check(input, expected, 112))
    def test_13(self):
        input = [
            "BEGIN",
            "INSERT a number",
            "BEGIN",
            "INSERT a number",
            "ASSIGN a 1",
            "END",
            "ASSIGN a 'str'",
            "END"
        ]
        expected = [
            "success", "success", "success", "TypeMismatch: ASSIGN a 'str'"
        ]
        self.assertTrue(TestUtils.check(input, expected, 113))

    def test_14(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "BEGIN",
            "INSERT x string",  # shadowing with new type
            "ASSIGN x 'abc'",
            "END",
            "ASSIGN x 123",
            "END"
        ]
        expected = [
            "success", "success", "Redeclared: INSERT x string", "TypeMismatch: ASSIGN x 'abc'", "success"
        ]
        self.assertTrue(TestUtils.check(input, expected, 114))

    def test_15(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "INSERT a string",
            "LOOKUP a",
            "END",
            "LOOKUP a",
            "END",
            "LOOKUP a",
            "END"
        ]
        expected = [
            "success","Redeclared: INSERT a string","0","0","0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 115))

    def test_16(self):
        input = [
            "INSERT a number",
            "INSERT b number",
            "ASSIGN a 10",
            "BEGIN",
            "INSERT c string",
            "ASSIGN c 'hi'",
            "BEGIN",
            "ASSIGN b 20",
            "ASSIGN d 30",
            "END",
            "END"
        ]
        expected = [
            "success","success","success","success","success","success","Undeclared: ASSIGN d 30"
        ]
        self.assertTrue(TestUtils.check(input, expected, 116))

    def test_17(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "INSERT a number",
            "BEGIN",
            "INSERT a number",
            "PRINT",
            "END",
            "PRINT",
            "END",
            "PRINT"
        ]
        expected = [
            "success","success","success","a//2","a//1","a//0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 117))

    def test_18(self):
        input = [
            "INSERT a number",
            "ASSIGN a 1",
            "BEGIN",
            "INSERT a string",
            "ASSIGN a 'hello'",
            "ASSIGN a 100", 
            "END",
            "ASSIGN a 5"
        ]
        expected = [
            "success","success","Redeclared: INSERT a string","TypeMismatch: ASSIGN a 'hello'","success","success"
        ]
        self.assertTrue(TestUtils.check(input, expected, 118))

    def test_19(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT y number",
            "ASSIGN x 10",
            "ASSIGN y 20",
            "END",
            "LOOKUP y",
            "LOOKUP x"
        ]
        expected = [
            "success", "success", "success", "success", "Undeclared: LOOKUP y","0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 119))

    def test_20(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "END",
            "END",
            "END",
            "END",
            "END",
            "END"
        ]
        expected = [
            "success", "UnknownBlock"
        ]
        self.assertTrue(TestUtils.check(input, expected, 120))

    def test_21(self):
        input = [
            "BEGIN",
            "BEGIN",
            "INSERT a number",
            "BEGIN",
            "INSERT b string",
            "END",
            "ASSIGN b 'test'",
            "END",
            "END"
        ]
        expected = [
            "success", "success", "Undeclared: ASSIGN b 'test'"
        ]
        self.assertTrue(TestUtils.check(input, expected, 121))

    def test_22(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "INSERT b number",
            "BEGIN",
            "INSERT c string",
            "PRINT",
            "END",
            "RPRINT",
            "END"
        ]
        expected = [
            "success", "success", "success","a//0 b//1 c//2", "b//1 a//0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 122))
