from unittest import TestCase
from unittest.mock import MagicMock, Mock

from sqlalchemy.exc import IntegrityError

from app.datalayer.models_file import FileManagerDataAccess
from app.services.exception_filemanager import FileAlreadyExistsError, FilePhysicalDbNotFoundError
from app.services.filemanager import FileManager


class TestFileManager(TestCase):
    __under_test = None

    def setUp(self):
        self.__under_test = FileManager(None)

    def test_general_signatures(self):
        self.assertRaises(NotImplementedError,
                          self.__under_test.upload_file, None, None)
        self.assertRaises(NotImplementedError,
                          self.__under_test.download_file_implementation, None)
        self.assertRaises(NotImplementedError,
                          self.__under_test.exists_file, None)

    def test_set_path(self):
        self.__under_test.set_path("/mypath")
        self.assertEqual(self.__under_test.get_path(), "/mypath")

    def test_download_file(self):
        session = MagicMock()
        session.query.filter.return_value = {}

        # mocking methods for my under test clas...
        under_test = FileManager(session)
        under_test.exists_file = MagicMock()
        under_test.exists_file.return_value = True
        under_test.download_file_implementation = MagicMock()

        under_test.download_file("john", "doe")

        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()

        under_test.download_file_implementation.assert_called_once_with("john")

    def test_download_notfound(self):
        session = MagicMock()
        session.query.filter.return_value = {}

        # mocking methods for my under test clas...
        under_test = FileManager(session)
        under_test.exists_file = MagicMock()
        under_test.exists_file.return_value = False

        self.assertRaises(FilePhysicalDbNotFoundError,
                          under_test.download_file, "dummy1", "dummy2")

    def test_new_upload(self):
        session = MagicMock()
        under_test = FileManager(session)
        under_test.exists_file = MagicMock()
        under_test.exists_file.return_value = False
        under_test.upload_file = MagicMock()

        under_test.upload(MagicMock(), MagicMock(), "my_file", False)

        session.query.assert_not_called()
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()

        under_test.upload_file.assert_called()

    def test_invalid_upload(self):
        under_test = FileManager(MagicMock())
        under_test.exists_file = MagicMock()
        under_test.exists_file.return_value = True
        under_test.upload_file = MagicMock()

        self.assertRaises(FileAlreadyExistsError, under_test.upload, MagicMock(), None, "123")

    def test_invalid_upload_file_exists(self):
        session = Mock()
        session.commit.side_effect = IntegrityError("xx", "xx", "xx")

        under_test = FileManager(session)
        under_test.exists_file = MagicMock()
        under_test.exists_file.return_value = False
        under_test.upload_file = MagicMock()

        self.assertRaises(FileAlreadyExistsError, under_test.upload, MagicMock(), None, "123")

        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_not_called()
        session.rollback.assert_called_once()

    def test_invalid_upload_replace_file(self):
        session = MagicMock()

        under_test = FileManager(session)
        under_test.exists_file = MagicMock()
        under_test.exists_file.return_value = False
        under_test.upload_file = MagicMock()
        session.query.filter.return_value = {}

        _buffer_mock = MagicMock()
        _buffer_mock.filename = "dummy"

        under_test.upload(_buffer_mock, None, "123", True)

        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()

        under_test.upload_file.assert_called_once_with("dummy", None)

    def test_not_found_file_db_upload_replace_file(self):
        session = Mock()
        session.query.return_value.filter.return_value.first.return_value = None

        under_test = FileManager(session)
        under_test.exists_file = MagicMock()
        under_test.exists_file.return_value = False
        under_test.upload_file = MagicMock()

        self.assertRaises(FilePhysicalDbNotFoundError, under_test.upload, MagicMock(), None, "123", True)

        session.add.assert_not_called()
        session.commit.assert_not_called()
        session.refresh.assert_not_called()

    def test_list_query(self):
        session = Mock()
        session.query.return_value = Mock()

        under_test = FileManager(session)
        under_test.list_files("123")

        session.query.assert_called_once_with(FileManagerDataAccess)
        session.query.return_value.filter.assert_called_once()
        session.query.return_value.filter.return_value.order_by.\
            assert_called_once()
        session.query.return_value.filter.return_value.order_by.\
            return_value.limit.assert_called_once_with(10)
        session.query.return_value.filter.return_value.order_by.return_value.\
            limit.return_value.all.assert_called_once()
