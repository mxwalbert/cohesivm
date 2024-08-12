from typing import Dict, Tuple
import pytest


def pytest_addoption(parser):
    # add commandline arguments for optional tests to be run
    parser.addoption('--ossila_x200', action='store_true', dest="ossila_x200", default=False,
                     help="Enable hardware tests for the Ossila X200 Source Measure Unit.")
    parser.addoption('--agilent_4284a', action='store_true', dest="agilent_4284a", default=False,
                     help="Enable hardware tests for the Agilent 4284A Precision LCR Meter.")
    parser.addoption('--agilent_4156c', action='store_true', dest="agilent_4284a", default=False,
                     help="Enable hardware tests for the Agilent 4156C Precision Semiconductor Parameter Analyzer.")
    parser.addoption('--ma8x8', action='store_true', dest="ma8x8", default=False,
                     help="Enable hardware tests for the MA8X8 Measurement Array 8x8 interface.")


def pytest_configure(config):
    # register markers for the hardware-dependent tests
    config.addinivalue_line(
        "markers", "hardware(name): mark tests to run only if the hardware is stated as commandline argument"
    )


# store history of failures per test class name and per index in parametrize (if parametrize used)
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    for hardware in [mark.args[0] for mark in item.iter_markers(name="hardware")]:
        if not item.config.getoption(hardware):
            pytest.skip(f"This test is only run if --{hardware} is given as commandline argument.")
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))

