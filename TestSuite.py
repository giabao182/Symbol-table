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
            "INSERT a number",
            "INSERT b number"
            "ASSIGN a b"
        ]
        expected = ["success"]*4
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
            "success", "success", "success", "success", "b//0 a//1 c//1", "a//0 b//0"
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
            "success", "success", "success", "success", "x//1 y//1 z//2", "UnclosedBlock: 3"
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
            "success", "success", "success", "success", "success"
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
            "success","success","3","0","0"
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
            "success","success","success","success","TypeMismatch: ASSIGN a 100","success"
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
    def test_23(self):
        input = [
            "INSERT x number",
            "BEGIN", "BEGIN", "BEGIN", "BEGIN", "BEGIN",  # 5 BEGIN
            "INSERT y string",
            "END", "END", "END", "END", "END"  # 5 END
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 123))
    def test_24(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT x string",
            "BEGIN",
            "INSERT x number",
            "PRINT",
            "END",
            "PRINT",
            "END",
            "PRINT"
        ]
        expected = [
            "success", "success", "success",
            "x//2", "x//1", "x//0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 124))
    def test_25(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "END",
            "ASSIGN x 5"
        ]
        expected = [
            "success", "Undeclared: ASSIGN x 5"
        ]
        self.assertTrue(TestUtils.check(input, expected, 125))
    def test_26(self):
        input = [
            "INSERT a number",
            "INSERT b string",
            "ASSIGN a 123",
            "ASSIGN b 'abc'",
            "ASSIGN b a",
            "ASSIGN a b"
        ]
        expected = [
            "success", "success", "success", "success",
            "TypeMismatch: ASSIGN b a", "TypeMismatch: ASSIGN a b"
        ]
        self.assertTrue(TestUtils.check(input, expected, 126))

    def test_27(self):
        input = [
            "INSERT a number",
            "ASSIGN a b"
        ]
        expected = [
            "success", "TypeMismatch: ASSIGN a b"
        ]
        self.assertTrue(TestUtils.check(input, expected, 127))
    def test_28(self):
        input = [
            "BEGIN",
            "BEGIN",
            "LOOKUP x",
            "END",
            "END"
        ]
        expected = ["Undeclared: LOOKUP x"]
        self.assertTrue(TestUtils.check(input, expected, 128))

    def test_29(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "END",
            "LOOKUP x"
        ]
        expected = ["success", "success", "1", "0"]
        self.assertTrue(TestUtils.check(input, expected, 129))

    def test_30(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "INSERT b number",
            "END",
            "ASSIGN a b"
        ]
        expected = ["success", "success", "TypeMismatch: ASSIGN a b"]
        self.assertTrue(TestUtils.check(input, expected, 130))

    def test_31(self):
        input = [
            "INSERT s string",
            "ASSIGN s 42"
        ]
        expected = ["success", "TypeMismatch: ASSIGN s 42"]
        self.assertTrue(TestUtils.check(input, expected, 131))

    def test_32(self):
        input = [
            "INSERT x number",
            "ASSIGN x 'string'"
        ]
        expected = ["success", "TypeMismatch: ASSIGN x 'string'"]
        self.assertTrue(TestUtils.check(input, expected, 132))

    def test_33(self):
        input = [
            "INSERT a number",
            "BEGIN", "INSERT b number",
            "BEGIN", "INSERT c number",
            "LOOKUP a", "LOOKUP b", "LOOKUP c",
            "END",
            "LOOKUP c",
            "END",
            "LOOKUP b"
        ]
        expected = [
            "success", "success", "success", "0", "1", "2",
            "Undeclared: LOOKUP c", "Undeclared: LOOKUP b"
        ]
        self.assertTrue(TestUtils.check(input, expected, 133))

    def test_34(self):
        input = [
            "INSERT x number",
            "ASSIGN x 1",
            "BEGIN",
            "INSERT x string",
            "ASSIGN x x",
            "END",
            "ASSIGN x x"
        ]
        expected = [
            "success", "success", "success",
            "TypeMismatch: ASSIGN x x", "TypeMismatch: ASSIGN x x"
        ]
        self.assertTrue(TestUtils.check(input, expected, 134))

    def test_35(self):
        input = [
            "BEGIN", "BEGIN", "BEGIN"
        ]
        expected = ["UnclosedBlock: 3"]
        self.assertTrue(TestUtils.check(input, expected, 135))

    def test_36(self):
        input = [
            "BEGIN", "END", "END"
        ]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 136))

    def test_37(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x y"
        ]
        expected = [
            "success", "success", "TypeMismatch: ASSIGN x y"
        ]
        self.assertTrue(TestUtils.check(input, expected, 137))

    def test_38(self):
        input = [
            "INSERT x number", "ASSIGN x 1",
            "BEGIN",
                "INSERT x number", "ASSIGN x 2",
                "BEGIN",
                    "INSERT x number", "ASSIGN x 3",
                    "LOOKUP x",
                "END",
                "LOOKUP x",
            "END",
            "LOOKUP x"
        ]
        expected = [
            "success", "success",
            "success", "success",
            "success", "success",
            "2", "1","0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 138))
    
    def test_39(self):
        input = [
            "BEGIN",
                "INSERT a number",
                "ASSIGN a 5",
            "END",
            "INSERT b number",
            "ASSIGN b a"
        ]
        expected = ["success", "success", "success", "TypeMismatch: ASSIGN b a"]
        self.assertTrue(TestUtils.check(input, expected, 139))

    def test_40(self):
        input = [
            "INSERT id number",
            "ASSIGN id 10",
            "BEGIN",
                "INSERT id string",
                "ASSIGN id 'abc'",
                "LOOKUP id",
            "END",
            "ASSIGN id 'xyz'"
        ]
        expected = [
            "success", "success",
            "success", "success", "1",
            "TypeMismatch: ASSIGN id 'xyz'"
        ]
        self.assertTrue(TestUtils.check(input, expected, 140))

    def test_41(self):
        input = [
            "BEGIN",
                "INSERT temp number",
            "END",
            "LOOKUP temp"
        ]
        expected = ["success", "Undeclared: LOOKUP temp"]
        self.assertTrue(TestUtils.check(input, expected, 141))

    def test_42(self):
        input = [
            "INSERT a number",
            "INSERT b number",
            "INSERT c number",
            "ASSIGN c 5",
            "ASSIGN b c",
            "ASSIGN a b"
        ]
        expected = ["success","success","success","success","TypeMismatch: ASSIGN b c","TypeMismatch: ASSIGN a b"] 
        self.assertTrue(TestUtils.check(input, expected, 142))

    def test_43(self):
        input = [
            "INSERT a number",
            "INSERT b string",
            "ASSIGN b 'hello'",
            "ASSIGN a b"
        ]
        expected = ["success", "success", "success", "TypeMismatch: ASSIGN a b"]
        self.assertTrue(TestUtils.check(input, expected, 143))

    def test_44(self):
        input = [
            "ASSIGN x 100"
        ]
        expected = ["Undeclared: ASSIGN x 100"]
        self.assertTrue(TestUtils.check(input, expected, 144))

    def test_45(self):
        input = [
            "INSERT s string",
            "ASSIGN s 'it\\'s complicated'"
        ]
        expected = ["success", "TypeMismatch: ASSIGN s 'it\\'s complicated'"]
        self.assertTrue(TestUtils.check(input, expected, 145))

    def test_46(self):
        input = [
            "INSERT x number",
            "ASSIGN x x"
        ]
        expected = ["success", "TypeMismatch: ASSIGN x x"]
        self.assertTrue(TestUtils.check(input, expected, 146))

    def test_47(self):
        input = [
            "INSERT x number",
            "BEGIN",
                "INSERT x number",
                "BEGIN",
                    "INSERT x number",
                    "LOOKUP x",
                "END",
                "LOOKUP x",
            "END",
            "LOOKUP x"
        ]
        expected = [
            "success", "success", "success", "2",
            "1",
            "0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 147))

    def test_48(self):
        input = [
            "INSERT x number",
            "BEGIN",
                "INSERT y number",
                "ASSIGN y 10",
                "ASSIGN x y",
            "END",
            "ASSIGN y 100"
        ]
        expected = [
            "success", "success", "success", "TypeMismatch: ASSIGN x y", "Undeclared: ASSIGN y 100"
        ]
        self.assertTrue(TestUtils.check(input, expected, 148))

    def test_49(self):
        input = [
            "INSERT a number",
            "ASSIGN a 1",
            "BEGIN",  # level 1
                "BEGIN",  # level 2
                    "INSERT b number",
                    "ASSIGN b 10",
                    "BEGIN",  # level 3
                        "INSERT c number",
                        "ASSIGN c 20",
                        "LOOKUP c",
                    "END",
                "END",
            "END"
        ]
        expected = ["success"] * 6 + ["3"]
        self.assertTrue(TestUtils.check(input, expected, 149))

    def test_50(self):
        input = [
            "INSERT v number", "ASSIGN v 0",
            "BEGIN", "INSERT v number", "ASSIGN v 1",
            "BEGIN", "INSERT v number", "ASSIGN v 2",
            "LOOKUP v", "END",
            "LOOKUP v", "END",
            "LOOKUP v"
        ]
        expected = [
            "success", "success",
            "success", "success",
            "success", "success",
            "2", "1", "0"
        ]
        self.assertTrue(TestUtils.check(input, expected, 150))