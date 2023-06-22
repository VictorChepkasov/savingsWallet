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

    function setWalletInfo(address _partyB) public payable onlyOwner {
        _withdraw(payable(address(this)), msg.value);
        walletInfo.partyB = payable(_partyB);
        walletInfo.partyBBad = false;
        walletInfo.timeLeft = 0;
        walletInfo.weiPerDay = address(this).balance / 100;
        allowances[msg.sender] = walletInfo.weiPerDay;
        allowances[walletInfo.partyB] = walletInfo.weiPerDay;
    }

    function _withdraw(address _to, uint _value) private {
        require(msg.sender != address(0), "Wrong address!");
        (bool sent, ) = _to.call{value: _value}("");
        require(sent, "Failed to send Ether");
    }

    function pay(address _to, uint _value) public payable setInfo {
        require(allowances[msg.sender] > 0, "You don't have money(");
        // allowances[msg.sender] -= _value;
        walletInfo.timeLeft = block.timestamp - walletInfo.timeLeft;
        _withdraw(_to, _value);
    }

    function updateLimit() public {
        require(walletInfo.timeLeft < block.timestamp , "Time has not run out yet");
        walletInfo.weiPerDay = address(this).balance / 100;
        allowances[walletInfo.owner] = walletInfo.weiPerDay;
        allowances[walletInfo.partyB] = walletInfo.weiPerDay;
        walletInfo.timeLeft = block.timestamp;
    }

    function getSavingWalletInfo() public view returns(
            WalletInfo memory, uint, uint
        ) {
        return (walletInfo,
            allowances[walletInfo.owner],
            allowances[walletInfo.partyB]
        );
    }

    function getWalletBalance() public view returns(uint) {
        return address(this).balance;
    }

    receive() external payable {}
    fallback() external payable {}

    modifier onlyOwner() {
        require(msg.sender == walletInfo.owner, 'Only Owner!');
        _;
    }

    modifier setInfo() {
        require(walletInfo.partyB != address(0), "Info not saved!");
        _;
    }
}