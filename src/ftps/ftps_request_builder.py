import os

from src.common.base_builder import BaseBuilder
from src.ftps.ftps_request import FtpsRequest
from src.ftps.ftps_service import FtpsService


class FtpsRequestBuilder(BaseBuilder):
    def __init__(self ):
        self.ftps_request = FtpsRequest()
        self.logger = None

    @classmethod
    def create(cls, setup):
        builder = cls()
        setup(builder)
        return builder
    
    def set_logger(self, logger):
        self.logger = logger
        return self

    def set_server(self, server):
        self.ftps_request.server = server
        return self

    def set_port(self, port):
        self.ftps_request.port = port
        return self
    def set_username(self, username):
        self.ftps_request.username = username
        return self

    def set_cert_file(self, cert_file):
        self.ftps_request.cert_file = cert_file
        return self
    def set_private_key_file(self, private_key_file):
        self.ftps_request.private_key_file = private_key_file
        return self
    def set_remote_path(self, remote_path):
        self.ftps_request.remote_file_path = remote_path
        return self

    def set_local_path(self, local_path):
        self.ftps_request.local_file_path = local_path
        return self
    
    def build(self):
        if  self.logger is None:
            self._create_default_console_logger()
        return self

    def send(self):
        self.build()
        self.validate_request(self.ftps_request)
        with FtpsService(self.ftps_request, logger=self.logger) as ftps_service:
            ftps_service.send()

    def validate_request(self, ftps_request):
        if ftps_request.server is None or "":
            raise Exception("Server cannot be empty");
        
        if ftps_request.port is None or "":
            raise Exception("Port cannot be empty");
    
        if  ftps_request.username is None or "" :
            raise Exception("UserName cannot be empty");
    
        if not os.path.exists(ftps_request.cert_file):
            raise Exception(f"Certificate file {ftps_request.cert_file} does not exist")

        if not os.path.exists(ftps_request.private_key_file):
            raise Exception(f"Private key file {ftps_request.private_key_file} does not exist")