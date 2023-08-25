// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "./savingsWallet.sol";

contract CloneFactory {
    function createClone(address _target) internal returns (address result) {
        bytes20 targetBytes = bytes20(_target);
        assembly {
            let clone := mload(0x40)
            mstore(clone, 0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000000000000000000000)
            mstore(add(clone, 0x14), targetBytes)
            mstore(add(clone, 0x28), 0x5af43d82803e903d91602b57fd5bf30000000000000000000000000000000000)
            result := create(0, clone, 0x37)
        }
    }

    function isClone(address _target, address _query) internal view returns (bool result) {
        bytes20 targetBytes = bytes20(_target);
        assembly {
            let clone := mload(0x40)
            mstore(clone, 0x363d3d373d3d3d363d7300000000000000000000000000000000000000000000)
            mstore(add(clone, 0xa), targetBytes)
            mstore(add(clone, 0x1e), 0x5af43d82803e903d91602b57fd5bf30000000000000000000000000000000000)

            let other := add(clone, 0x40)
            extcodecopy(_query, other, 0, 0x2d)
            result := and(
                eq(mload(clone), mload(other)),
                eq(mload(add(clone, 0xd)), mload(add(other, 0xd)))
            )
        }
    }
}

contract WalletsFactory is CloneFactory {
    address payable masterContract;
    uint public walletsCounter = 0;
    mapping(uint => SavingWallet) public savingWallets;

    constructor(address payable _masterContract) {
        masterContract = _masterContract;
    }

    function getSavingWallet(uint _walletId) external view returns(SavingWallet) {
        return savingWallets[_walletId];
    }

    function createWallet(
        ERC20 _weth,
        address _owner,
        address _partyB,
        uint _amount
    )
        public
    {
        SavingWallet savingWallet = SavingWallet(
            payable(createClone(masterContract))
        );
        _weth.transferFrom(msg.sender, address(savingWallet), _amount);
        walletsCounter += 1;
        savingWallet.init(_weth, _owner, _partyB, walletsCounter);
        savingWallets[walletsCounter] = savingWallet;
    }
}