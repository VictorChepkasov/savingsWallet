import pytest
from brownie import accounts
from scripts.deploySavingWallet import deploySavingWallet
from test_value_manipulation import walletContract
from scripts.scripts import (
    setWalletInfo,
    updateWalletBalance,
    updateLimit,
    getWalletInfo,
    getWalletBalance,
)

pytestmark = pytest.mark.parametrize('deposit', [0, 50, 100, 200000])

def test_setWalletInfo(walletContract, deposit):
    owner, b, _ = walletContract
    deploySavingWallet(owner)
    validInfo = [owner.address, b.address, deposit // 100,
        0, False, deposit // 100, deposit // 100]
    setWalletInfo(owner, b, deposit)
    testInfo = getWalletInfo()
    print(f'Valid: {validInfo}')
    assert testInfo == validInfo

def test_updateLimit(walletContract, deposit):
    owner, b, _ = walletContract
    setWalletInfo(owner, b, deposit)
    validInfo = getWalletInfo()
    validInfo = [validInfo[-1], validInfo[-2]]
    updateLimit()
    newInfo = getWalletInfo()
    newInfo = [newInfo[-1], newInfo[-2]]
    assert validInfo == newInfo

def test_updateWalletBalance(walletContract, deposit):
    owner, b, _ = walletContract
    initialDeposit = 500
    setWalletInfo(owner, b, initialDeposit)
    validBalance = initialDeposit + deposit
    updateWalletBalance(deposit)
    updatedBalance = getWalletBalance()
    assert updatedBalance == validBalance