class FtpsRequest:
    def __init__(self):
        self.server = None
        self.port = 990
        self.username = None
        self.cert_file = None
        self.private_key_file = None
        
        self.remote_file_path = None
        self.local_file_path = None

        self.local_files_path = None
        self.local_dir = None
        self.file_pattern = None


