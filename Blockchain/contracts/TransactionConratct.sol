pragma solidity ^0.5.16;

contract Investing {
    struct Startup {
        string name;
        uint expectedAmount;
        address owner;
        bool isTokenized;
    }

    mapping(address => uint256) public Investments;
    mapping(address => Startup) public startups; 
    address[] public startupAddresses; 

    event StartupRegistered(address indexed owner, string name, uint expectedAmount);
    event InvestmentMade(address indexed investor, address indexed startupAddress, string investorName, uint amount);

    function register(string memory startupName, uint expectedAmount) public {
        require(expectedAmount > 0, "Expected amount must be greater than 0");

        startups[msg.sender] = Startup(startupName, expectedAmount, msg.sender, true);
        startupAddresses.push(msg.sender);

        emit StartupRegistered(msg.sender, startupName, expectedAmount);
    }

    function invest(address startupAddress, string memory investorName, uint amount) public {
        require(startups[startupAddress].isTokenized, "Startup must be registered before investment");
        

        Investments[msg.sender] += amount;

        emit InvestmentMade(msg.sender, startupAddress, investorName, amount);
    }
}
