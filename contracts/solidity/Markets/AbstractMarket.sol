pragma solidity 0.4.11;
import "Events/AbstractEvent.sol";
import "MarketMakers/AbstractMarketMaker.sol";


/// @title Abstract market contract - Functions to be implemented by market contracts
contract Market {

    address public creator;
    uint public createdAtBlock;
    Event public eventContract;
    MarketMaker public marketMaker;
    uint public fee;
    uint public funding;
    int[] public netOutcomeTokensSold;
    function fund(uint _funding) public;
    function close() public;
    function withdrawFees() public returns (uint);
    function buy(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint maxCost) public returns (uint);
    function sell(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint minProfit) public returns (uint);
    function shortSell(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint minProfit) public returns (uint);
    function calcMarketFee(uint outcomeTokenCost) public constant returns (uint);
}
