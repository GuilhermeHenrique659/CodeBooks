class ValidationFile:

    ALLOWED_IMAGE = ['png','jpg','jfif','gif','jpeg']
    ALLOWED_VIDEO = ['mp4']

    def type_file(self, filename:str) -> str:
        return filename.rsplit('.', 1)[1].lower()

    def isImageValid(self, file_extension:str) -> bool:
        if file_extension in self.ALLOWED_IMAGE:
            return True
        else:
            return False

    def isVideoValid(self, file_extension:str) -> bool:
        if file_extension in self.ALLOWED_VIDEO:
            return True
        else:
            return False

validation_file = ValidationFile()