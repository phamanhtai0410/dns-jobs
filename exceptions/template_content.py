
class TemplateContentNotFoundEx(Exception):
    def __init__(self, msg='Template Content Not Found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TEMPLATE_CONTENT_NOT_FOUND'

    pass

class UserNotOwnTemplateEx(Exception):
    def __init__(self, msg='User Not Own Template', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_USER_NOT_TEMPLATE'

    pass

class DomainNotFoundEx(Exception):
    def __init__(self, msg='Domain Not Found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_DOMAIN_NOT_FOUND'

    pass