// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./WETH.sol";

contract SavingWallet is ReentrancyGuard {
    using SafeERC20 for ERC20;

    struct WalletInfo {
        address owner;
        address partyB;
        uint id;
        uint weiPerDay; //wei на день
        uint timeLeft; //последний день обновления лимита
        /*uint8 rewardB награда стороны B, 
        устанавливается по желанию owner в процентах*/
        bool partyBBad; //злонамернность стороны B
    }
    
    mapping(address => uint) allowances; //оставшееся кол-во денег у сторон
    mapping(address => bool) consents; //нельзя получить через геттеры! Лень.

    ERC20 public WETH;
    WalletInfo public walletInfo;

    modifier onlyOwner() {
        require(msg.sender == walletInfo.owner, 'Only Owner!');
        _;
    }

    modifier onlyParties() {
        require(
            msg.sender == walletInfo.owner || msg.sender == walletInfo.partyB,
            "Only parties!"
        );
        _;
    }

    modifier setConsents() {
        require(
            consents[walletInfo.owner] == consents[walletInfo.partyB] == true,
            "You need an consent!"
        );
        _;
    }

    constructor() {}

    receive() external payable {}
    fallback() external payable {}

    // функция вместо конструктора, т.к. мы используем createClone
    function init(
        ERC20 _WETH,
        address _owner,
        address _partyB,
        uint _id
    ) 
        external 
    {
        require(
            _partyB != _owner,
            "Party B and Owner must be different people!"
        );
        require(_partyB != address(0), "Incorrect party B address!");
        
        WETH = _WETH;

        walletInfo.owner = _owner;
        walletInfo.partyB = _partyB;

        walletInfo.id = _id;
        walletInfo.partyBBad = false;
        walletInfo.timeLeft = block.timestamp;
        walletInfo.weiPerDay = WETH.balanceOf(address(this)) / 100;
        allowances[walletInfo.owner] = walletInfo.weiPerDay;
        allowances[walletInfo.partyB] = walletInfo.weiPerDay;
        consents[walletInfo.owner] = false;
        consents[walletInfo.partyB] = false;
    }

    function getSavingWalletInfo() external view returns(WalletInfo memory, uint, uint) {
        return (
            walletInfo,
            allowances[walletInfo.owner],
            allowances[walletInfo.partyB]
        );
    }

    function getWalletBalance() external view returns(uint) {
        return WETH.balanceOf(address(this));
    }

    function setConsentToBreakLimit() external onlyParties {
        consents[msg.sender] = true;
    }

    function updateWalletBalance(uint _amount) external onlyOwner nonReentrant {
        WETH.transferFrom(msg.sender, address(this), _amount);
        walletInfo.weiPerDay = WETH.balanceOf(address(this)) / 100;
        allowances[walletInfo.owner] = walletInfo.weiPerDay;
        allowances[walletInfo.partyB] = walletInfo.weiPerDay;
        walletInfo.timeLeft = block.timestamp;
    }

    function pay(address _to, uint _amount) public onlyParties nonReentrant {
        require(allowances[msg.sender] > 0, "You don't have money(");
        require(
            _amount <= walletInfo.weiPerDay && _amount <= allowances[msg.sender],
            "You don't have money per day("
        );
        if (walletInfo.timeLeft + uint(1 days) <= block.timestamp) {
            updateLimit();
        }
        allowances[msg.sender] -= _amount;
        WETH.transfer(_to, _amount);
    }

    function breakTheLimit(address _to, uint _amount) public setConsents nonReentrant {
        require(
            _amount > walletInfo.weiPerDay,
            "You aren't breaking the limit!"
        );
        require(
            WETH.balanceOf(address(this)) >= _amount,
            "You don't have money("
        );
        WETH.transfer(_to, _amount);
        if (WETH.balanceOf(address(this)) / 100 > 0) {
            walletInfo.weiPerDay = WETH.balanceOf(address(this)) / 100;
            allowances[walletInfo.owner] = walletInfo.weiPerDay;
            allowances[walletInfo.partyB] = walletInfo.weiPerDay;
            walletInfo.timeLeft = block.timestamp;
        }
    }

    function blockPartyB() public onlyOwner {
        walletInfo.partyBBad = true;
        allowances[msg.sender] = 0;
        allowances[walletInfo.partyB] = 0;
        WETH.transfer(walletInfo.owner, WETH.balanceOf(address(this)));
    }

    function updateLimit() public {
        require(
            walletInfo.timeLeft + uint(1 days) <= block.timestamp, 
            "Time has not run out yet"
        );
        allowances[walletInfo.owner] = walletInfo.weiPerDay;
        allowances[walletInfo.partyB] = walletInfo.weiPerDay;
        walletInfo.timeLeft = block.timestamp;
    }
}