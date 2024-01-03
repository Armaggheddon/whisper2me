class ResultWithData():

    def __init__(
        self,
        is_success = False,
        message = "",
        data = None
    ):
        self.is_success = is_success
        self.message = message
        self.data = data