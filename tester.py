
import data_processor
from dataclasses import dataclass
import sys
from typing import Any


WHITE = "\033[97m"
YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
FAILED = f"{RED}[Failed]{RESET}"
SUCCES = f"{GREEN}[Succes]{RESET}"

def main() -> None:

    match len(sys.argv):
        case 1:
            normal_tests()

        case 2:
            if sys.argv[1] in ("-h", "--help"):
                print("Flags:\n"
                      "--normal for a standard tests\n"
                      "--strict for everything I could come up with")
                return
            else:
                print("Use ./tester.py --help")
                return

        case _:
            print("Use ./tester.py --help")
            return


def testing_func(test_cases: tuple[dict]) -> list:

    full_res = []
    for case in test_cases:

        # Puts the arguments in proper values to have it more structured
        results = []
        func = case["func"]
        tests = case["tests"]
        expected = case["expected"]
        should_raise = case["should_raise"]
        message = case["message"]
        testing_message = case["testing_message"]

        print(f"\n{testing_message}")

        if isinstance(expected, tuple):
            expected_iter = expected
        else:
            # This makes it so you can just pase in one expected value for all tests
            expected_iter = [expected] * len(tests)
        for test, expect in zip(tests, expected_iter):
            try:
                # if the test input is not a tuple already make it one (Makes it less work)
                if not isinstance(test, tuple):
                    test = (test,)
                results.append(func(*test))
            except Exception as e:
                results.append(e)
            finally:
                if results[-1] == expect or (should_raise and isinstance(results[-1], Exception)):
                    full_res.append(True)
                    print(f"| {SUCCES} ", end='')
                else:
                    full_res.append(False)
                    print(f"| {FAILED} ", end='')
                print(
                    f"{message:<25} "
                    f"{repr(test):<25} "
                    f"Expected: {str(expect):<10} "
                    f"Got: {str(results[-1])}"
                )
    return full_res


def numericProcesor_tests_0() -> None:
    print("Testing numericProcesor")
    print("-----------------------")

    num_proc0 = data_processor.NumericProcessor()
    num_proc1 = data_processor.NumericProcessor()
    num_proc2 = data_processor.NumericProcessor()
    numeric_tests = (
        {
            "func": num_proc0.validate,
            "tests": (42, 1.2, -1000, -2.5, [12, 0.33, -12]),
            "expected": True,
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to verify valid input"
        },
        {
            "func": num_proc0.validate,
            "tests": ("12", "abc", {0: 12}, True, ["abc", True]),
            "expected": False,
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to verify unvalid input"
        },
        {
            "func": num_proc0.ingest,
            "tests": ("12", "abc", {0: 12}, True, ["abc", True]),
            "expected": "[Costum error message]",
            "should_raise": True,
            "message": "Trying to ingest input: ",
            "testing_message": "Trying to ingest unvalid input"
        },
        {
            "func": num_proc1.ingest,
            "tests": (42, 1.2, -1000, -2.5, [12, 0.33, -12]),
            "expected": None,
            "should_raise": False,
            "message": "Trying to ingest input: ",
            "testing_message": "Trying to ingest valid input"
        },
        {
            "func": num_proc1.output,
            "tests": (((),) * 7),
            "expected": ((0, "42"), (1, "1.2"), (2, "-1000"), (3, "-2.5"), (4, "12"), (5, "0.33"), (6, "-12")),
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to get output"
        },
        {
            "func": num_proc2.output,
            "tests": (((),) * 4),
            "expected": ((-1, "No data available"),),
            "should_raise": False,
            "message": "Calling output on empty data: ",
            "testing_message": "Trying to get output"
        }
    )
    res = testing_func(numeric_tests)
    return res


def textProcesor_tests_0() -> None:
    print("Testing textProcesor")
    print("-----------------------")

    text_proc0 = data_processor.TextProcessor()
    text_proc1 = data_processor.TextProcessor()
    text_proc2 = data_processor.TextProcessor()

    text_tests = (
        {
            "func": text_proc0.validate,
            "tests": ("Hello", "1.2", "Wont", "!", ["abc", "0.33", "Banana"]),
            "expected": True,
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to verify valid input"
        },
        {
            "func": text_proc0.validate,
            "tests": (12, -12, {0: 12}, True, ["abc", 2]),
            "expected": False,
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to verify unvalid input"
        },
        {
            "func": text_proc0.ingest,
            "tests": (12, -12, {0: 12}, True, ["abc", 2]),
            "expected": "[Costum error message]",
            "should_raise": True,
            "message": "Trying to ingest input: ",
            "testing_message": "Trying to ingest unvalid input"
        },
        {
            "func": text_proc1.ingest,
            "tests": ("Hello", "1.2", "Wont", "!", ["abc", "0.33", "Banana"]),
            "expected": None,
            "should_raise": False,
            "message": "Trying to ingest input: ",
            "testing_message": "Trying to ingest valid input"
        },
        {
            "func": text_proc1.output,
            "tests": (((),) * 7),
            "expected": ((0, "Hello"), (1, "1.2"), (2, "Wont"), (3, "!"), (4, "abc"), (5, "0.33"), (6, "Banana")),
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to get output"
        },
        {
            "func": text_proc2.output,
            "tests": (((),) * 4),
            "expected": ((-1, "No data available"),),
            "should_raise": False,
            "message": "Calling output on empty data: ",
            "testing_message": "Trying to get output"
        }
    )
    res = testing_func(text_tests)
    return res


def logProcesor_tests_0() -> None:
    print("Testing logProcesor")
    print("-----------------------")

    log_proc0 = data_processor.LogProcessor()
    log_proc1 = data_processor.LogProcessor()
    log_proc2 = data_processor.LogProcessor()

    # Think about giving in a list as well lots of cursed stuff
    text_tests = (
        {
            "func": log_proc0.validate,
            "tests": (
                {"log_level": "READ", "log_message" : "Something bad"},
                {"log_message": "It should", "log_level" : "Still works?"},
                [
                    {"log_level": "READ", "log_message" : "Something bad"},
                    {"log_level": "BAD", "log_message" : "Overflow"}
                ]),
            "expected": True,
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to verify valid input"
        },
        {
            "func": log_proc0.validate,
            "tests": (
                {"log_level": "READ", "log_message" : 12},
                {"log_message": -12, "log_level" : "Still works?"},
                12, "hello", [{"log_level": "READ", "log_message" : 12}]),
            "expected": False,
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to verify unvalid input"
        },
        {
            "func": log_proc0.ingest,
            "tests": (
                {"log_level": "READ", "log_message" : 12},
                {"log_message": -12, "log_level" : "Still works?"},
                12, "hello", [{"log_level": "READ", "log_message" : 12}]),
            "expected": "[Costum error message]",
            "should_raise": True,
            "message": "Trying to ingest input: ",
            "testing_message": "Trying to ingest unvalid input"
        },
        {
            "func": log_proc1.ingest,
            "tests": (
                {"log_level": "READ", "log_message" : "Something bad"},
                {"log_message": "It should", "log_level" : "Still works?"},
                [
                    {"log_level": "READ", "log_message" : "Something bad"},
                    {"log_level": "BAD", "log_message" : "Overflow"}
                ]),
            "expected": None,
            "should_raise": False,
            "message": "Trying to ingest input: ",
            "testing_message": "Trying to ingest valid input"
        },
        {
            "func": log_proc1.output,
            "tests": (((),) * 4),
            "expected": ((0, 'READ: Something bad'), (1, 'Still works?: It should'), (2, 'READ: Something bad'), (3, 'BAD: Overflow')),
            "should_raise": False,
            "message": "Trying to verify input: ",
            "testing_message": "Trying to get output"
        },
        {
            "func": log_proc2.output,
            "tests": (((),) * 4),
            "expected": ((-1, "No data available"),),
            "should_raise": False,
            "message": "Calling output on empty data: ",
            "testing_message": "Trying to get output"
        }
    )
    res = testing_func(text_tests)
    return res


def normal_tests() -> None:
    trys = []
    score = 0
    for i in numericProcesor_tests_0():
        trys.append(i)
    print()
    for i in textProcesor_tests_0():
        trys.append(i)
    print()
    for i in logProcesor_tests_0():
        trys.append(i)

    for i in trys:
        if i is True:
            score += 1
    
    print()
    print(f"Got {score}/{len(trys)}")


if __name__ == "__main__":
    main()

# ! Add the key check