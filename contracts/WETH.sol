// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract WrappedETH is ERC20 {
    using SafeERC20 for ERC20;

    constructor(address emiter) ERC20("Wrapped Ether", "WETH") {}

    function mint(address to, uint amount) external {
        require(amount > 0, "You can't mint 0 tokens!");
        _mint(to, amount);
    }

    function burn(address to, uint amount) external {
        require(amount > 0, "You can't burn 0 tokens!");
        _burn(to, amount);
    }
}

contract WETHFactory {
    address payable public owner;
    ERC20 public token;

    constructor() {
        owner = payable(msg.sender);
        token = new WrappedETH(address(this));
    }

    receive() external payable {
        uint tokenToBuy = msg.value; //1 eth == 1 token
        require(tokenToBuy > 0, "Not enough funds!");
        WrappedETH(address(token)).mint(msg.sender, tokenToBuy);
    }

    function sell(uint _amountToSell) external {
        require(
            _amountToSell > 0 && token.balanceOf(msg.sender) >= _amountToSell,
            "Incorrect amount!"
        );
        uint allowance = token.allowance(msg.sender, address(this));
        require(allowance >= _amountToSell, "Check allowance!");
        WrappedETH(address(token)).burn(msg.sender, _amountToSell);
        payable(msg.sender).transfer(_amountToSell);
    }

    function tokenBalance() public view returns(uint) {
        return token.balanceOf(address(this));
    }

    modifier onlyOwner() {
        require(owner == msg.sender, "Only owner!");
        _;
    }
}