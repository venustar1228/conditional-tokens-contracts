pragma solidity 0.4.11;
import "Tokens/StandardToken.sol";


/// @title Outcome token contract - Issuing and revoking outcome tokens
/// @author Stefan George - <stefan@gnosis.pm>
contract OutcomeToken is StandardToken {
    using Math for *;

    /*
     *  Events
     */
    event Issue(address indexed owner, uint amount);
    event Revoke(address indexed owner, uint amount);

    /*
     *  Storage
     */
    address public eventContract;

    /*
     *  Modifiers
     */
    modifier isEventContract () {
        // Only event contract is allowed to proceed
        require(msg.sender == eventContract);
        _;
    }

    /*
     *  Public functions
     */
    /// @dev Constructor sets events contract address
    function OutcomeToken()
        public
    {
        eventContract = msg.sender;
    }
    
    /// @dev Events contract issues new tokens for address. Returns success
    /// @param _for Address of receiver
    /// @param outcomeTokenCount Number of tokens to issue
    function issue(address _for, uint outcomeTokenCount)
        public
        isEventContract
    {
        balances[_for] = balances[_for].add(outcomeTokenCount);
        totalSupply = totalSupply.add(outcomeTokenCount);
        Issue(_for, outcomeTokenCount);
    }

    /// @dev Events contract revokes tokens for address. Returns success
    /// @param _for Address of token holder
    /// @param outcomeTokenCount Number of tokens to revoke
    function revoke(address _for, uint outcomeTokenCount)
        public
        isEventContract
    {
        balances[_for] = balances[_for].sub(outcomeTokenCount);
        totalSupply = totalSupply.sub(outcomeTokenCount);
        Revoke(_for, outcomeTokenCount);
    }
}
