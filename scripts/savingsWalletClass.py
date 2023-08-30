from brownie import SavingWallet, WalletsFactory, WETHFactory, WrappedETH

class SavingsWallet:
    def __init__(self, _wallet):
        self.wallet = _wallet
        self.address = _wallet.address
        self.OwnerAddress = _wallet.getSavingWalletInfo()[0][0]

    def getWalletInfo(self):
        info = self.wallet.getSavingWalletInfo()
        walletInfo = list(info[:-2][0])
        walletInfo.append(info[1])
        walletInfo.append(info[2])
        print(f"Wallet info: {walletInfo}")
        return walletInfo
    
    def getWalletBalance(self):
        balance = self.wallet.getWalletBalance()
        print(f'Balance contract: {balance}')
        return balance
    
    def updateWalletBalance(self, _amount):
        self.wallet.updateWalletBalance(_amount, {
            'from': self.OwnerAddress,
            'priority_fee': '10 wei'
        })

    def updateLimit(self):
        self.wallet.updateLimit({
            'from': self.OwnerAddress,
            'priority_fee': '10 wei'
        })
        
    def setConsentToBreakLimit(self, _from):
        self.wallet.setConsentToBreakLimit({
            'from': _from,
            'priority_fee': '10 wei'
        })
        print(f'{self.OwnerAddress} consent to break the limit!')

    def pay(self, _to, _amount):
        print('Person sending tokens')
        self.wallet.pay(_to, _amount, {
            'from': self.OwnerAddress,
            'priority_fee': '10 wei'
        })
        print('Person send tokens')

    def breakTheLimit(self, _to, _amount):
        self.wallet.breakTheLimit(_to, _amount, {
            'from': self.OwnerAddress,
            'priority_fee': '10 wei'
        })
        print('Party send Ether (break limit)!')

    def blockPartyB(self):
        self.wallet.blockPartyB({
            'from': self.OwnerAddress,
            'priority_fee': '10 wei'
        })
        print('Party B blocked!')