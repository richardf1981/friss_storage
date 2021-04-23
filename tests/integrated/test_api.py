import os
os.environ["TEST"] = "True"

from main import app
from unittest import TestCase
from fastapi.testclient import TestClient
import os

client = TestClient(app)
path_dummy_file = 'tests/integrated/media/dummy.pdf'


class TestApi(TestCase):

    def test_download_api_not_found(self):
        response = client.get(
            "/api/v1/file_download?file_name=non_existent_file.xpto")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "File not found"})

    def test_upload_and_download(self):
        # should remove file if exists...
        with open(path_dummy_file, "rb") as f:
            response = client.post("/api/v1/file_upload",
                                   files={"file": ("dummy1.pdf", f,
                                                   "application/pdf")})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "done"})

        response_download = client.get(
            "/api/v1/file_download?file_name=dummy1.pdf")
        self.assertEqual(response_download.status_code,
                         200)

    def test_upload_already_exists(self):
        with open(path_dummy_file, "rb") as f:
            response = client.post("/api/v1/file_upload",
                                   files={"file": ("dummy1.pdf", f,
                                                   "application/pdf")})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "done"})

            # tries do upload same file...
            response = client.post("/api/v1/file_upload",
                                   files={"file": ("dummy1.pdf", f,
                                                   "application/pdf")})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(),
                             {'detail': 'File already exists'})

    def test_put_patch_non_existent_file(self):
        with open(path_dummy_file, "rb") as f:
            response = client.put("/api/v1/file_upload",
                                  files={"file": ("non_existent.pdf", f,
                                                  "application/pdf")})
            self.assertEqual(response.status_code,
                             404)
            self.assertEqual(response.json(),
                             {"detail": "File not found, unable to replace"})

            response = client.patch("/api/v1/file_upload",
                                    files={"file": ("non_existent.pdf",
                                                    f, "application/pdf")})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json(),
                             {"detail": "File not found, unable to replace"})

    @staticmethod
    def remove_file():
        if os.path.exists("media/dummy1.pdf"):
            os.remove("media/dummy1.pdf")

    def tearDown(self):
        self.remove_file()

    def setUp(self):
        self.remove_file()
