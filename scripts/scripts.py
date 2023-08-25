from brownie import SavingWallet, WalletsFactory, WETHFactory, WrappedETH

def getSavingWallet(_walletId):
    savingWallet = WalletsFactory[-1].getSavingWallet(_walletId)
    return SavingWallet.at(savingWallet)

def getSavigWallets(_startId, _endId):
    walletsArr = []
    for i in range(_startId, _endId+1):
        savingWallet = WalletsFactory[-1].getSavingWallet(i)
        walletsArr.append(savingWallet)
    return walletsArr

def getWalletInfo(_from, wallet):
    info = wallet.getSavingWalletInfo({
        'from': _from,
        'priority_fee': '10 wei'
    })
    walletInfo = list(info[:-2][0])
    walletInfo.append(info[1])
    walletInfo.append(info[2])
    print(f"Wallet info: {walletInfo}")
    return walletInfo

def getWalletBalance(wallet):
    balance = wallet.getWalletBalance()
    print(f'Balance contract: {balance}')
    return balance

def updateWalletBalance(_from, _amount, wallet):
    wallet.updateWalletBalance(_amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    
def setConsentToBreakLimit(_from, wallet):
    wallet.setConsentToBreakLimit({
        'from': _from,
        'priority_fee': '10 wei'
    })
    print(f'{_from} consent to break the limit!')

def createWallet(_weth, _from, _partyB, _amount):
    WalletsFactory[-1].createWallet(_weth, _from, _partyB, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print('Saving wallet created!')

def pay(_from, _to, _amount, wallet):
    print('Person sending tokens')
    wallet.pay(_to, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print('Person send tokens')

def breakTheLimit(_from, _to, _amount, wallet):
    wallet.breakTheLimit(_to, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    print('Party send Ether (break limit)!')

def blockPartyB(wallet):
    wallet.blockPartyB({
        'priority_fee': '10 wei'
    })
    print('Party B blocked!')

def approve(_from, _spenderAddress, _amount):
    WrappedETH.at(WETHFactory[-1].token()).approve(_spenderAddress, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })

def buyWETH(_from, _tokenAddress, _amountToBuy):
    _from.transfer(_tokenAddress, f'{_amountToBuy} wei', priority_fee='10 wei')