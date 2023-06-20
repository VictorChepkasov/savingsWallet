from brownie import SavingWallet

def setWalletInfo(_owner, _partyB):
    SavingWallet[-1].setWalletInfo(_partyB, {
        'from': _owner,
        'priority_fee': '10 wei'
    })
    print('Set saving wallet info!')

def updateLimit():
    SavingWallet.updateLimit()
    print('Limit updated!')

def getSavingWalletInfo():
    info = SavingWallet[-1].getSavingWalletInfo()
    walletInfo = list(info[:-2])
    walletInfo.append(info[1])
    walletInfo.append(info[2])
    return walletInfo

def withdraw(_to, _value):
    print(f'{_to} sending Ether')
    SavingWallet[-1].withdraw(_to, _value, {
        'value': _value,
        'priority_fee': '10 wei'
    })
    print(f'{_to} send Ether')