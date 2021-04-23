import os
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from app.services.filesystem_managers import FileSystemManager


class TestFileSystemManager(TestCase):
    __under_test = None

    def setUp(self):
        self.__under_test = FileSystemManager(Mock())
        self.__under_test.set_path("/mypath")

    def test_exists_file(self):
        with patch.object(os.path, "exists", return_value=True) \
                as mock_method:
            self.__under_test.exists_file("path")
            mock_method.assert_called_once()
            self.assertEqual(mock_method.return_value, True)

        with patch.object(os.path, "exists", return_value=False) \
                as mock_method:
            self.__under_test.exists_file("/mypath")
            mock_method.assert_called_once()
            self.assertEqual(mock_method.return_value, False)

    # TODO: refactor this method...
    # def test_upload_method(self):
    #     with patch("builtins.open", mock_open(read_data="data")) as mock_file:
    #         with patch.object(shutil, "copyfileobj") as mock_shutil:
    #             self.__under_test.upload_file("", None)
    #             mock_shutil.assert_called_once()
    #             mock_file.assert_called_with("/mypath", "wb")

    def test_download_file(self):
        self.__under_test.exists_file = MagicMock()
        self.__under_test.set_path("any")
        self.__under_test.exists_file.return_value = True

        ret = self.__under_test.download_file("dummy_file", "123")
        self.assertEqual(self.__under_test.get_path() + "dummy_file", ret[0])
