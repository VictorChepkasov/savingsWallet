from brownie import SavingWallet

def setWalletInfo(_owner, _partyB, _deposit):
    SavingWallet[-1].setWalletInfo(_partyB, {
        'from': _owner,
        'value': f'{_deposit} wei',
        'priority_fee': '10 wei'
    })
    print('Set saving wallet info!')

def updateLimit():
    SavingWallet.updateLimit()
    print('Limit updated!')

def getWalletInfo():
    info = SavingWallet[-1].getSavingWalletInfo()
    walletInfo = list(info[:-2][0])
    walletInfo.append(info[1])
    walletInfo.append(info[2])
    print(f"Wallet info: {walletInfo}")
    return walletInfo

def pay(_to, _value):
    print(f'{_to} sending Ether')
    SavingWallet[-1].pay(_to, _value, {
        'value': _value,
        'priority_fee': '10 gwei'
    })
    print(f'{_to} send Ether')

def getWalletBalance():
    balance = SavingWallet[-1].getWalletBalance()
    print(f'Balance contract: {balance}')
    return balance

def updateWalletBalance(_deposit):
    SavingWallet[-1].updateWalletBalance({
        'value': _deposit,
        'priority_fee': '10 wei'
    })