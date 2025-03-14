""" Module for configuring tests """

from faker import Faker


def pytest_addoption(parser):
    """ Defines a command line option in pytest """
    parser.addoption(
        "--num_records",
        action="store",
        default="100",
        help="Number of records to use in tests"
    )


def gen_rnd_cmd():
    """ Generates a random command to test parsing """
    fake = Faker()
    fake_command = {"command": fake.word(), "num_args": fake.random_digit()}
    args = []
    fake_command["args"] = {}
    for i in range(1, fake_command["num_args"] + 1):
        fake_command["args"][f"argument_{i}"] = fake.word()
        args.append(fake_command["args"][f"argument_{i}"])
    fake_command["input_str"] = " ".join([fake_command["command"]] + args)
    return fake_command


def pytest_generate_tests(metafunc):
    """ Auto-generate test via hook in pytest """
    # cli_input is used for testing command parser
    if "cli_input" in metafunc.fixturenames:
        num_records = int(metafunc.config.getoption("--num_records"))
        testdata = [gen_rnd_cmd() for _ in range(num_records)]
        metafunc.parametrize("cli_input", testdata)
