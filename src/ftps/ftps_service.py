import ftplib
import os
import ssl
from typing import List

from src.ftps.ftps_request import FtpsRequest


class FtpsService:

    def __init__(self, ftps_request: FtpsRequest, logger):
        self.ftps = None
        self.ftps_request = ftps_request
        self.logger = logger

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        try:
            self.logger.info(f"Connecting to FTPS server {self.ftps_request.server}")
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=self.ftps_request.cert_file, keyfile=self.ftps_request.private_key_file)
            self.ftps = ftplib.FTP_TLS(context=context)
            self.ftps.connect(self.ftps_request.server, self.ftps_request.port)
            self.ftps.login(self.ftps_request.username)
            self.ftps.prot_p()
        except Exception as e:
            self.logger.error(f"Error connecting to FTPS server: {e}")
            raise

    def disconnect(self):
        if self.ftps:
            try:
                self.ftps.quit()
            except Exception as e:
                self.logger.error(f"Error disconnecting from FTPS server: {e}")
                raise
            finally:
                self.ftps = None

    def send(self):
        """Send single file to FTPS server"""
        remote_file_path = self.ftps_request.remote_file_path or os.path.basename(self.ftps_request.local_file_path)
        self._upload_file(self.ftps_request.local_file_path, remote_file_path)

    def send_files(self):
        """Send multiple files to FTPS server"""
        if self.ftps_request.local_files_path:
            self._upload_multiple_files(self.ftps_request.local_files_path)
        elif self.ftps_request.local_dir:
            self._upload_directory_files(self.ftps_request.local_dir, self.ftps_request.file_pattern)

    def _upload_file(self, local_path: str, remote_path: str):
        try:
            with open(local_path, 'rb') as f:
                self.ftps.storbinary(f'STOR {remote_path}', f)
            self.logger.info(f"File {local_path} uploaded successfully")
        except Exception as e:
            self.logger.error(f"Error uploading file {local_path}: {e}")
            raise

    def _upload_multiple_files(self, files: List[str]):
        for file in files:
            self._upload_file(file, os.path.basename(file))

    def _upload_directory_files(self, directory: str, pattern: str):
        for file in os.listdir(directory):
            if file.endswith(pattern):
                local_path = os.path.join(directory, file)
                self._upload_file(local_path, file)

