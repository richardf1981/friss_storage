import os

from ..services.filemanager import FileManager

COPY_BUFFER_SIZE = 1024 * 1024


class FileSystemManager(FileManager):

    def exists_file(self, file_name):
        return os.path.exists("{}{}".format(self.get_path(), str(file_name)))

    def download_file_implementation(self, file_name):
        return "{}{}".format(self.get_path(), file_name)

    def upload_file(self, file_name, buffer_out):
        tot_bytes = 0
        with open(self.get_path() + file_name, "wb") as bytes_f:
            while True:
                buf = buffer_out.read(COPY_BUFFER_SIZE)
                tot_bytes += len(buf)
                if not buf:
                    break
                bytes_f.write(buf)

        return tot_bytes
