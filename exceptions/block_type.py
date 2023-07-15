
class BlockTypeNotSameEx(Exception):
    def __init__(self, msg='Block', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_BLOCK_TYPE_NOT_SAME'

    pass
