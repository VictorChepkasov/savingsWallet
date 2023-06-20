// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract SavingWallet {
    struct WalletInfo {
        address payable owner;
        address payable partyB;
        uint weiPerDay; //wei на день
        uint timeLeft; //оставшееся время до обновления лимита
        /*uint8 rewardB награда стороны B, 
        устанавливается по желанию owner в процентах*/
        bool partyBBad; //злонамернность стороны B
        //оставшееся кол-во денег у сторон
    }
    mapping(address => uint) allowances; 

    WalletInfo private walletInfo;

    constructor() {
        walletInfo.owner = payable(msg.sender);
    }

    /*
        Большая часть кода будет переписана. 
        это лишь наброски того, как всё должно рбаотать
    */

    function setWalletInfo(address _partyB) public onlyOwner {
        walletInfo.partyB = payable(_partyB);
        walletInfo.weiPerDay = address(this).balance / 100;
        walletInfo.partyBBad = false;
        updateLimit();
    }

    function withdraw(address _to, uint _value) public payable {
        require(msg.sender != address(0), "Wrong address!");
        allowances[msg.sender] -= msg.value;
        walletInfo.timeLeft = block.timestamp - walletInfo.timeLeft;
        (bool sent, ) = _to.call{value: _value}("");
        require(sent, "Failed to send Ether");
    }

    function updateLimit() internal {
        require(walletInfo.timeLeft - block.timestamp <= 0, "Time hasn't run out yet");
        allowances[walletInfo.owner] = walletInfo.weiPerDay;
        allowances[walletInfo.partyB] = walletInfo.weiPerDay;
        walletInfo.timeLeft = block.timestamp;
    }

    function getSavingWalletInfo() public view returns(
            WalletInfo memory, uint, uint
        ) {
        return (walletInfo, allowances[walletInfo.owner], allowances[walletInfo.partyB]);
    }

    receive() external payable {}
    fallback() external payable {}

    modifier onlyOwner() {
        require(msg.sender == walletInfo.owner, 'Only Owner!');
        _;
    }
}