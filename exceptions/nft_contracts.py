
class NftContractNotFoundEx(Exception):
    def __init__(self, msg='Nft contract not found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NFT_CONTRACT_NOT_FOUND'

    pass

class NftIndexTypeNotFound(Exception):
    def __init__(self, msg='Nft Index Type Not Found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NFT_INDEX_NOT_FOUND'

    pass

class NftContractNotCreateFromInzEx(Exception):
    def __init__(self, msg='Nft Contract Not Create From Inz', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NFT_CONTRACT_NOT_CREATE_FROM_INZ'

    pass
