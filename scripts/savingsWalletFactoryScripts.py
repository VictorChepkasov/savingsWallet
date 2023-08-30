from brownie import SavingWallet, WalletsFactory, WETHFactory, WrappedETH

def createWallet(_weth, _from, _partyB, _amount):
    walletId = WalletsFactory[-1].createWallet(_weth, _from, _partyB, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    }).return_value
    print('Saving wallet created!')
    return walletId

def getSavingWallet(_from, _walletId):
    savingWallet = WalletsFactory[-1].getSavingWallet(_walletId, {
        'from': _from,
        'priority_fee': '10 wei'
    })
    return SavingWallet.at(savingWallet)

def getSavigWallets(_startId, _endId):
    walletsArr = []
    for i in range(_startId, _endId+1):
        savingWallet = WalletsFactory[-1].getSavingWallet(i)
        walletsArr.append(savingWallet)
    return walletsArr

def approve(_from, _spenderAddress, _amount):
    WrappedETH.at(WETHFactory[-1].token()).approve(_spenderAddress, _amount, {
        'from': _from,
        'priority_fee': '10 wei'
    })

def buyWETH(_from, _tokenAddress, _amountToBuy):
    _from.transfer(_tokenAddress, f'{_amountToBuy} wei', priority_fee='10 wei')