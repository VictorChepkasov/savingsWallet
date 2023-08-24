// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "./savingsWallet.sol";

contract WalletsFactory {
    mapping(uint => SavingWallet) public savingWallets;
    uint public walletsCounter = 0;

    constructor() {}

    function getSavingWallet(uint walletId) external view returns(SavingWallet) {
        return savingWallets[walletId];
    }

    function createWallet(address _partyB) public {
        SavingWallet savingWallet = new SavingWallet(_partyB, ++walletsCounter);
        walletsCounter += 1;
        savingWallets[walletsCounter] = savingWallet;
    }
}