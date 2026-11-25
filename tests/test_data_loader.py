
import numpy as np
import pandas as pd
import pytest

from g61.data_loader import load_subject, get_imu


@pytest.fixture
def sample_data(tmp_path):
    """Create a small artificial PAMAP2 file."""

    data = np.zeros((2, 54))

    # First row: transient activity
    data[0, 1] = 0

    # Second row: walking activity
    data[1, 1] = 4

    # Wrist accelerometer
    data[1, 4:7] = [1.0, 2.0, 3.0]

    # Wrist gyroscope
    data[1, 10:13] = [0.1, 0.2, 0.3]

    path = tmp_path / "subject101.dat"

    pd.DataFrame(data).to_csv(
        path,
        sep=" ",
        header=False,
        index=False
    )

    return tmp_path


def test_load_subject(sample_data):
    df = load_subject(101, data_dir=sample_data)

    assert df.shape == (1, 54)
    assert df["activity_id"].iloc[0] == 4


def test_keep_transient(sample_data):
    df = load_subject(
        101,
        data_dir=sample_data,
        remove_transient=False
    )

    assert len(df) == 2


def test_wrist_accelerometer(sample_data):
    df = load_subject(101, data_dir=sample_data)

    acc = get_imu(df, "wrist")

    assert acc.iloc[0].tolist() == [1.0, 2.0, 3.0]


def test_wrist_gyroscope(sample_data):
    df = load_subject(101, data_dir=sample_data)

    gyro = get_imu(
        df, "wrist", "gyroscope"
    )

    assert np.allclose(
        gyro.iloc[0].to_numpy(),
        [0.1, 0.2, 0.3]
    )


def test_invalid_subject():
    with pytest.raises(ValueError):
        load_subject(999)


def test_invalid_location(sample_data):
    df = load_subject(101, data_dir=sample_data)

    with pytest.raises(ValueError):
        get_imu(df, "head")
