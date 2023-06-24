from brownie import SavingWallet, accounts

def main():
    owner = accounts[0]
    b = accounts[1]
    c = accounts[2]
    contract = SavingWallet.deploy({
        'from': owner,
        "priority_fee": '10 gwei'
    })
    setWalletInfo(owner, b, 100000000)
    pay(c, 100000)
    getWalletBalance()

def setWalletInfo(_owner, _partyB, _deposit):
    SavingWallet[-1].setWalletInfo(_partyB, {
        'from': _owner,
        'value': f'{_deposit} wei',
        'gas_price': '10 wei'
    })
    print('Set saving wallet info!')

def setConsentToBreakLimit(_from):
    SavingWallet[-1].setConsentToBreakLimit({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'{_from} consent to break the limit!')

def pay(_to, _value):
    print('Person sending Ether')
    SavingWallet[-1].pay(_to, _value, {
        'priority_fee': '10 wei'
    })
    print('Person send Ether')

def breakTheLimit(_to, _value):
    SavingWallet[-1].breakTheLimit(_to, _value, {
        'priority_fee': '100 wei'
    })
    print('Party send Ether (break limit)!')

def updateWalletBalance(_deposit):
    SavingWallet[-1].updateWalletBalance({
        'value': _deposit,
        'priority_fee': '10 wei'
    })

def updateLimit():
    SavingWallet[-1].updateLimit({
        'priority_fee': '10 wei'
    })
    print(f'''
          Limit updated!
          Owner: {getWalletInfo()[-1]}
          Party B: {getWalletInfo()[-2]}
          ''')

def getWalletInfo():
    info = SavingWallet[-1].getSavingWalletInfo()
    walletInfo = list(info[:-2][0])
    walletInfo.append(info[1])
    walletInfo.append(info[2])
    print(f"Wallet info: {walletInfo}")
    return walletInfo

def getWalletBalance():
    balance = SavingWallet[-1].getWalletBalance()
    print(f'Balance contract: {balance}')
    return balance