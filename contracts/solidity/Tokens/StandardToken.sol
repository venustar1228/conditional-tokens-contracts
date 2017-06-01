pragma solidity 0.4.11;
import "Tokens/AbstractToken.sol";
import "Utils/Math.sol";


/// @title Standard token contract with overflow protection
contract StandardToken is Token {

    /*
     *  Storage
     */
    mapping (address => uint) balances;
    mapping (address => mapping (address => uint)) allowances;
    uint public totalSupply;

    /*
     *  Public functions
     */
    /// @dev Transfers sender's tokens to a given address. Returns success
    /// @param to Address of token receiver
    /// @param value Number of tokens to transfer
    /// @return Returns success of function call
    function transfer(address to, uint value)
        public
        returns (bool)
    {
        if (   !Math.safeToSub(balances[msg.sender], value)
            || !Math.safeToAdd(balances[to], value))
            return false;
        balances[msg.sender] -= value;
        balances[to] += value;
        Transfer(msg.sender, to, value);
        return true;
    }

    /// @dev Allows allowed third party to transfer tokens from one address to another. Returns success
    /// @param from Address from where tokens are withdrawn
    /// @param to Address to where tokens are sent
    /// @param value Number of tokens to transfer
    /// @return Returns success of function call
    function transferFrom(address from, address to, uint value)
        public
        returns (bool)
    {
        if (   !Math.safeToSub(balances[from], value)
            || !Math.safeToSub(allowances[from][msg.sender], value)
            || !Math.safeToAdd(balances[to], value))
            return false;
        balances[from] -= value;
        allowances[from][msg.sender] -= value;
        balances[to] += value;
        Transfer(from, to, value);
        return true;
    }

    /// @dev Sets approved amount of tokens for spender. Returns success
    /// @param spender Address of allowed account
    /// @param value Number of approved tokens
    /// @return Returns success of function call
    function approve(address spender, uint value)
        public
        returns (bool)
    {
        allowances[msg.sender][spender] = value;
        Approval(msg.sender, spender, value);
        return true;
    }

    /// @dev Returns number of allowed tokens for given address
    /// @param owner Address of token owner
    /// @param spender Address of token spender
    /// @return Returns remaining allowance for spender
    function allowance(address owner, address spender)
        public
        constant
        returns (uint)
    {
        return allowances[owner][spender];
    }

    /// @dev Returns number of tokens owned by given address
    /// @param owner Address of token owner
    /// @return Returns balance of owner
    function balanceOf(address owner)
        public
        constant
        returns (uint)
    {
        return balances[owner];
    }
}
