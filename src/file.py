class FileOpenMock:

    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data

    def write(self):
        pass

    def writelines(self):
        pass

    def close(self):
        pass
