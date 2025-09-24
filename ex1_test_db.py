import os
import pickle
from unittest.mock import patch, mock_open
from mydb import MyDB

def test_creates_empty_database_if_file_does_not_exist():

    # SETUP
    patch_isfile = patch('os.path.isfile', return_value=False)
    patch_open = patch('builtins.open', mock_open())
    patch_dump = patch('pickle.dump')

    mock_isfile = patch_isfile.start()
    mock_open_func = patch_open.start()
    mock_dump = patch_dump.start()

    # EXERCISE
    try:
        db = MyDB("mydatabase.db")

    # VERIFY
        mock_isfile.assert_called_once_with("mydatabase.db")
        mock_open_func.assert_called_once_with("mydatabase.db", 'wb')
        mock_dump.assert_called_once_with([], mock_open_func.return_value)

    # TEARDOWN
    finally:
        patch_isfile.stop()
        patch_open.stop()
        patch_dump.stop()