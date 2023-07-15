class NameServicesNotFoundException(Exception):
    def __init__(self, msg='Name services not found.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NAME_SERVICES_NOT_FOUND'

    pass
