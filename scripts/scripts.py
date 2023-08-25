from brownie import SavingWallet, WalletsFactory

def getSavingWallet(walletId):
    savingWallet = WalletsFactory[-1].getSavingWallet(walletId)
    return SavingWallet.at(savingWallet)

def getSavigWallets(startId, endId):
    walletsArr = []
    for i in range(startId, endId+1):
        savingWallet = WalletsFactory[-1].getSavingWallet(i)
        walletsArr.append(savingWallet)
    return walletsArr

def getWalletInfo(wallet):
    info = wallet.getSavingWalletInfo()
    walletInfo = list(info[:-2][0])
    walletInfo.append(info[1])
    walletInfo.append(info[2])
    print(f"Wallet info: {walletInfo}")
    return walletInfo

def getWalletBalance(wallet):
    balance = wallet.getWalletBalance()
    print(f'Balance contract: {balance}')
    return balance

def updateWalletBalance(_deposit, wallet):
    wallet.updateWalletBalance({
        'value': f'{_deposit} wei',
        'priority_fee': '10 wei'
    })

def updateLimit(wallet):
    wallet.updateLimit({
        'priority_fee': '10 wei'
    })
    print(f'''
          Limit updated!
          Owner: {getWalletInfo()[-1]}
          Party B: {getWalletInfo()[-2]}
          ''')
    
def setConsentToBreakLimit(_from, wallet):
    wallet.setConsentToBreakLimit({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'{_from} consent to break the limit!')

def createWallet(_from, partyB, value):
    WalletsFactory[-1].createWallet(_from, partyB, {
        'from': _from,
        'value': f"{value} wei",
        'priority_fee': '10 wei'
    })
    print('Saving wallet created!')

def pay(_from, _to, _value, wallet):
    print('Person sending Ether')
    wallet.pay(_to, {
        'from': _from,
        'value': _value,
        'priority_fee': '10 wei'
    })
    print('Person send Ether')

def breakTheLimit(_to, _value, wallet):
    wallet.breakTheLimit(_to, _value, {
        'priority_fee': '100 wei'
    })
    print('Party send Ether (break limit)!')

def blockPartyB(wallet):
    wallet.blockPartyB({
        'priority_fee': '10 wei'
    })
    print('Party B blocked!')