class NftTradeOwnerAddressCanNotEqualToAddress(Exception):
    def __init__(self, msg='owner address can not equal to address', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_OWNER_ADDRESS_CAN_NOT_EQUAL_TO_ADDRESS'

    pass
