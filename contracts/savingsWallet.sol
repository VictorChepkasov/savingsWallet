// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract savingWallet {
    struct WalletInfo {
        address payable owner;
        address payable partyB;

        uint128 weiPerDay;
        uint128 weiPerSecond;
        uint128 allowance;
        uint8 lastSendTime;
        // uint8 rewardB награда стороны B, устанавливается по желанию owner в процентах

        bool partyBBad; //злонамернность стороны B
    }

    WalletInfo private walletInfo;

    constructor() {
        walletInfo.owner = payable(msg.sender);
    }

    //устанавливаем лимит. Возможно, перенесу код в другую функцию
    function limit() public {
        walletInfo.weiPerDay = uint128(address(this).balance / 100);
        walletInfo.weiPerSecond = uint128(walletInfo.weiPerDay / uint(1 days));
        walletInfo.allowance = walletInfo.weiPerDay;
    }

    //обновление лимита, скорее всего перепишу
    function update() public {
        walletInfo.allowance += uint8(walletInfo.weiPerSecond + (walletInfo.lastSendTime - block.timestamp));
        if (walletInfo.allowance > walletInfo.weiPerDay) {
            walletInfo.allowance = walletInfo.weiPerDay;
        }
        walletInfo.lastSendTime = uint8(block.timestamp);
    }

    function setWalletInfo(
        address payable _partyB
    ) public onlyOwner {
        walletInfo.partyB = _partyB;
        walletInfo.lastSendTime = uint8(block.timestamp);
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