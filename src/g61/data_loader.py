
from pathlib import Path

import pandas as pd


# Repository root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Default PAMAP2 dataset location
DATA_DIR = PROJECT_ROOT / "data" / "PAMAP2_Dataset" / "Protocol"


# PAMAP2 IMU columns (zero-based indexing)
IMU_COLUMNS = {
    "wrist": {
        "accelerometer": [4, 5, 6],
        "gyroscope": [10, 11, 12],
    },
    "chest": {
        "accelerometer": [21, 22, 23],
        "gyroscope": [27, 28, 29],
    },
    "ankle": {
        "accelerometer": [38, 39, 40],
        "gyroscope": [44, 45, 46],
    },
}


def load_subject(subject_id, data_dir=DATA_DIR,
                 remove_transient=True):
    """
    Load PAMAP2 protocol data for one subject.

    Parameters
    ----------
    subject_id : int
        Subject ID between 101 and 109.
    data_dir : str or Path
        Folder containing subjectXXX.dat files.
    remove_transient : bool
        Remove activity ID 0 if True.

    Returns
    -------
    pandas.DataFrame
        Loaded sensor measurements.
    """

    if subject_id not in range(101, 110):
        raise ValueError("Subject ID must be 101-109.")

    file_path = (
        Path(data_dir) / f"subject{subject_id}.dat"
    )

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )

    df = pd.read_csv(
        file_path,
        sep=r"\s+",
        header=None
    )

    if df.shape[1] != 54:
        raise ValueError(
            f"Expected 54 columns, got {df.shape[1]}"
        )

    df = df.rename(columns={
        0: "timestamp",
        1: "activity_id",
        2: "heart_rate"
    })

    if remove_transient:
        df = df[df["activity_id"] != 0].copy()

    return df.reset_index(drop=True)


def get_imu(df, location, sensor_type="accelerometer"):
    """
    Extract IMU measurements for a body location.
    """

    location = location.lower()
    sensor_type = sensor_type.lower()

    if location not in IMU_COLUMNS:
        raise ValueError(
            "Location must be wrist, chest or ankle."
        )

    if sensor_type not in IMU_COLUMNS[location]:
        raise ValueError(
            "Sensor type must be accelerometer or gyroscope."
        )

    columns = IMU_COLUMNS[location][sensor_type]

    return df[columns].copy()
