
import data_processor
import sys
import typing


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

def testing_func(expected_out: list, tests: list,
                 func: typing.Callable) -> list[bool]:

    results = []
    for test, expected in zip(tests, expected_out):
        result = func(test)
        if result != expected:
            print(f"[Failed] Expected: {expected} got: {result}")
            results.append(result)
        else:
            print(f"[Succes] Expected: {expected} got: {result}")
            results.append(result)
    return results

def normal_tests() -> None:
    valid_list = [12, 0.33, -12]
    valid_nums = [42, 1.2, -1000, -2.5, valid_list]

    expected = [True, True, True, True, True]
    num_proc = data_processor.NumericProcessor()
    testing_func(expected, valid_nums, num_proc.validate)
    # numericProcessor_tests()


def numericProcessor_tests() -> None:
    # Creating instance of NumericProcessor
    num_proc = data_processor.NumericProcessor()

    print("\nTesting valid input on validation")
    print("---------------------------------")
    valid_list = [12, 0.33, -12]
    valid_nums = [42, 1.2, -1000, -2.5, valid_list]
    for x in valid_nums:
        result = num_proc.validate(x)
        if result is not True:
            print("| Fail: ", end='')
        else:
            print("| Succes: ", end='')

        print(f"Trying to validate input: {str(x):<15} -> "
              f"{result}")

    print("\nTesting unvalid input on validation")
    unvalid_list = ["abc", True]
    unvalid_input = ["12", "abc", {0: 12}, True, unvalid_list]
    for x in unvalid_input:
        print(f"| Trying to validate input: {str(x):<15} -> "
              f"{num_proc.validate(x)}")

    print("\nTesting invalid ingestion without prior validation:")
    unvalid_list = ["abc", True]
    unvalid_input = ["12", "abc", {0: 12}, True, unvalid_list]
    for x in unvalid_input:
        try:
            print(f"| Trying to ingest input: {str(x):<15} -> "
                  f"{num_proc.ingest(x)}")
        except Exception as e:
            print(f"| {str(e):>15}: '{str(x)}'")

    print("\nTesting valid ingestion")
    valid_list = [12, 0.33, -12]
    valid_nums = [42, 1.2, -1000, -2.5, valid_list]
    for x in valid_nums:
        print(f"| Trying to ingestion input: {str(x):<15}")
        num_proc.ingest(x)

    print("\nTesting valid extraction")
    for _ in valid_nums:
        print(f"| Extracting: {num_proc.output()}")


if __name__ == "__main__":
    main()


