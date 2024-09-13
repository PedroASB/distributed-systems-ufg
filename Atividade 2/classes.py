class Address:
    def __init__(self, street: str, neighborhood: str, number: int):
        self.street = street
        self.neighborhood = neighborhood
        self.number = number

    def __repr__(self):
        return f"Address(street='{self.street}', neighborhood='{self.neighborhood}', number={self.number})"


class BankDetails:
    def __init__(self, bank: str, agency: str, account: str):
        self.bank = bank
        self.agency = agency
        self.account = account

    def __repr__(self):
        return f"BankDetails(bank='{self.bank}', agency='{self.agency}', account='{self.account}')"


class Person:
    def __init__(self, name: str, address: Address, bank_details: BankDetails):
        self.name = name
        self.address = address
        self.bank_details = bank_details

    def __repr__(self):
        return (f"Person(name='{self.name}', address={self.address}, "
                f"bank_details={self.bank_details})")
