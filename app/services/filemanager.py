import uuid

from sqlalchemy.exc import IntegrityError

from ..datalayer.models_file import FileManagerDataAccess, FileManagerHistory
from ..services.exception_filemanager import FileAlreadyExistsError, \
    FilePhysicalDbNotFoundError


class FileManager(object):
    __path = None
    __session = None

    def __init__(self, session):
        self.__session = session

    def __save_new(self, file_obj, size_bytes, user_id):
        file_manager_data = FileManagerDataAccess(
            file_name=u'{}'.format(file_obj.filename),
            mime_type=file_obj.content_type,
            file_size=size_bytes,
            user_id_created=user_id)

        try:
            self.__session.add(file_manager_data)
            self.__session.commit()
            self.__session.refresh(file_manager_data)
        except IntegrityError:
            self.__session.rollback()
            raise FileAlreadyExistsError()

    def __save_history(self, file_obj, size_bytes, user_id):
        file_manager_data = self.__session.query(FileManagerDataAccess). \
            filter(FileManagerDataAccess.file_name == file_obj.filename). \
            first()

        if not file_manager_data:
            raise FilePhysicalDbNotFoundError()

        file_manager_data_history = FileManagerHistory(
            id_file=file_manager_data.id,
            user_id_updated=user_id,
            file_size=size_bytes,
            type_access="update")
        self.__session.add(file_manager_data_history)
        self.__session.commit()
        self.__session.refresh(file_manager_data)

    def set_path(self, path):
        self.__path = path

    def get_path(self):
        return self.__path

    def upload_file(self, file_name, buffer_out):
        raise NotImplementedError()

    def download_file_implementation(self, file_name):
        raise NotImplementedError()

    def download_file(self, file_name, user_id):
        file_manager_data = self.__session.query(FileManagerDataAccess). \
            filter(file_name == file_name).first()

        if not self.exists_file(file_name) or \
                not file_manager_data:
            raise FilePhysicalDbNotFoundError()

        file_manager_data_history = FileManagerHistory(
            id=uuid.uuid4(),
            id_file=file_manager_data.id,
            user_id_updated=user_id,
            type_access="download")

        self.__session.add(file_manager_data_history)
        self.__session.commit()
        self.__session.refresh(file_manager_data_history)

        return self.download_file_implementation(
            file_name), file_manager_data.mime_type

    def exists_file(self, file_name):
        raise NotImplementedError()

    def upload(self, file_obj, buffer_file_out, user_id,
               replace_file=False):
        if self.exists_file(file_obj.filename) and replace_file is False:
            raise FileAlreadyExistsError()

        size_bytes = self.upload_file(file_obj.filename, buffer_file_out)

        if replace_file:
            self.__save_history(file_obj, size_bytes, user_id)
        else:
            self.__save_new(file_obj, size_bytes, user_id)

    def list_files(self, user_id, limit=10):
        return self.__session.query(FileManagerDataAccess). \
            filter(FileManagerDataAccess.user_id_created == user_id).\
            order_by(FileManagerDataAccess.created_date.desc()).limit(limit).all()
