import time
from unittest.mock import MagicMock
from cohesivm.experiment import Experiment
from cohesivm.data_stream import DataStream
from cohesivm.progressbar import ProgressBar


def test_progressbar():
    """Test the ProgressBar class functionality."""
    # Mock the Experiment and its attributes
    experiment_mock = MagicMock(spec=Experiment)
    experiment_mock.selected_contacts = ["contact1", "contact2"]
    experiment_mock.measurement.output_shape = (10,)
    experiment_mock.data_stream = DataStream()

    # Create ProgressBar instance
    pbar = ProgressBar(experiment_mock)

    # Assertions to validate initialization
    assert pbar.num_contacts == 2
    assert pbar.num_datapoints == 10

    # Test the show context manager
    with pbar.show():
        # Simulate data being added to the data_stream
        for _ in range(2):
            for __ in range(10):
                pbar.data_stream.put("data_point")
                time.sleep(0.2) # allow the thread to update the pbar

        # Ensure the pbar was closed
        assert pbar.data_stream.empty()

        # Simulate termination
        pbar.close()
        time.sleep(0.2) # allow the thread to update the pbar

        # Ensure the terminate string was used
        assert not pbar.data_stream.empty()
        assert pbar.data_stream.get() == pbar.terminate_string
