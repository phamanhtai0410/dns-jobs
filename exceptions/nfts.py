class UserNotOwnNftEx(Exception):
    def __init__(self, msg='User not own nft', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_USER_NOT_OWN_NFT'

    pass


class CurrencyTokenNotExceptEx(Exception):
    def __init__(self, msg='Currency Token Not Except', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_CURRENCY_TOKEN_NOT_ACCEPT'

    pass


class NftIsOnMarketEx(Exception):
    def __init__(self, msg='Nft is on market', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NFT_IS_ON_MARKET'

    pass


class NftIsNotOnMarketEx(Exception):
    def __init__(self, msg='Nft is not on market', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NFT_IS_NOT_ON_MARKET'

    pass


class NftNotFoundEx(Exception):
    def __init__(self, msg='Nft not found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NFT_NOT_FOUND'

    pass
