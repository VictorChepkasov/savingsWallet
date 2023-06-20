// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract savingWallet {
    struct WalletInfo {
        address payable owner;
        address payable partyB;

        uint weiPerDay;
        uint weiPerSecond;
        uint allowance; //оставшееся кол-во денег
        uint lastSendTime;
        //uint8 rewardB награда стороны B, устанавливается по желанию owner в процентах

        bool partyBBad; //злонамернность стороны B
    }

    WalletInfo private walletInfo;

    constructor() {
        walletInfo.owner = payable(msg.sender);
    }

    /*
        Большая часть кода будет переписана, 
        это лишь наброски того, как всё должно рбаотать
    */

    function limit() public {
        walletInfo.weiPerDay = address(this).balance / 100;
        walletInfo.weiPerSecond = walletInfo.weiPerDay / uint(1 days);
        walletInfo.allowance = walletInfo.weiPerDay;
    }

    function update() public {
        walletInfo.allowance += walletInfo.weiPerSecond + (walletInfo.lastSendTime - block.timestamp);
        if (walletInfo.allowance > walletInfo.weiPerDay) {
            walletInfo.allowance = walletInfo.weiPerDay;
        }
        walletInfo.lastSendTime = block.timestamp;
    }

    function setWalletInfo(
        address payable _partyB
    ) public onlyOwner {
        walletInfo.partyB = _partyB;
        walletInfo.lastSendTime = block.timestamp;
        walletInfo.partyBBad = false;
    }

    function _withdraw(address _to, uint _value) private {
        require(msg.sender != address(0), "Wrong address!");
        (bool sent, ) = _to.call{value: _value}("");
        require(sent, "Failed to send Ether");
    }

    modifier onlyOwner() {
        require(msg.sender == walletInfo.owner, 'Only Owner!');
        _;
    }
}