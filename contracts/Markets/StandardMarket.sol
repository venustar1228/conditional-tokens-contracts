pragma solidity 0.4.15;
import "../Markets/Market.sol";
import "../Tokens/Token.sol";
import "../Events/Event.sol";
import "../MarketMakers/MarketMaker.sol";

contract StandardMarketProxy is MarketProxy {
    /*
     *  Constants
     */
    uint24 public constant FEE_RANGE = 1000000; // 100%

    function StandardMarketProxy(address proxy, address _creator, Event _eventContract, MarketMaker _marketMaker, uint24 _fee)
        MarketProxy(proxy)
        public
    {
        // Validate inputs
        require(address(_eventContract) != 0 && address(_marketMaker) != 0 && _fee < FEE_RANGE);
        creator = _creator;
        createdAtBlock = block.number;
        eventContract = _eventContract;
        netOutcomeTokensSold = new int[](eventContract.getOutcomeCount());
        fee = _fee;
        marketMaker = _marketMaker;
        stage = Market.Stages.MarketCreated;
    }
}


/// @title Standard market contract - Backed implementation of standard markets
/// @author Stefan George - <stefan@gnosis.pm>
contract StandardMarket is Market {
    using Math for *;

    /*
     *  Constants
     */
    uint24 public constant FEE_RANGE = 1000000; // 100%

    /*
     *  Modifiers
     */
    modifier isCreator() {
        // Only creator is allowed to proceed
        require(msg.sender == creator);
        _;
    }

    modifier atStage(Stages _stage) {
        // Contract has to be in given stage
        require(stage == _stage);
        _;
    }

    /*
     *  Public functions
     */
    /// @dev Allows to fund the market with collateral tokens converting them into outcome tokens
    /// @param _funding Funding amount
    function fund(uint _funding)
        public
        isCreator
        atStage(Stages.MarketCreated)
    {
        // Request collateral tokens and allow event contract to transfer them to buy all outcomes
        require(   eventContract.collateralToken().transferFrom(msg.sender, this, _funding)
                && eventContract.collateralToken().approve(eventContract, _funding));
        eventContract.buyAllOutcomes(_funding);
        funding = _funding;
        stage = Stages.MarketFunded;
        MarketFunding(funding);
    }

    /// @dev Allows market creator to close the markets by transferring all remaining outcome tokens to the creator
    function close()
        public
        isCreator
        atStage(Stages.MarketFunded)
    {
        uint8 outcomeCount = eventContract.getOutcomeCount();
        for (uint8 i = 0; i < outcomeCount; i++)
            require(eventContract.outcomeTokens(i).transfer(creator, eventContract.outcomeTokens(i).balanceOf(this)));
        stage = Stages.MarketClosed;
        MarketClosing();
    }

    /// @dev Allows market creator to withdraw fees generated by trades
    /// @return Fee amount
    function withdrawFees()
        public
        isCreator
        returns (uint fees)
    {
        fees = eventContract.collateralToken().balanceOf(this);
        // Transfer fees
        require(eventContract.collateralToken().transfer(creator, fees));
        FeeWithdrawal(fees);
    }

    /// @dev Allows to buy outcome tokens from market maker
    /// @param outcomeTokenIndex Index of the outcome token to buy
    /// @param outcomeTokenCount Amount of outcome tokens to buy
    /// @param maxCost The maximum cost in collateral tokens to pay for outcome tokens
    /// @return Cost in collateral tokens
    function buy(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint maxCost)
        public
        atStage(Stages.MarketFunded)
        returns (uint cost)
    {
        // Calculate cost to buy outcome tokens
        uint outcomeTokenCost = marketMaker.calcCost(this, outcomeTokenIndex, outcomeTokenCount);
        // Calculate fees charged by market
        uint fees = calcMarketFee(outcomeTokenCost);
        cost = outcomeTokenCost.add(fees);
        // Check cost doesn't exceed max cost
        require(cost > 0 && cost <= maxCost);
        // Transfer tokens to markets contract and buy all outcomes
        require(   eventContract.collateralToken().transferFrom(msg.sender, this, cost)
                && eventContract.collateralToken().approve(eventContract, outcomeTokenCost));
        // Buy all outcomes
        eventContract.buyAllOutcomes(outcomeTokenCost);
        // Transfer outcome tokens to buyer
        require(eventContract.outcomeTokens(outcomeTokenIndex).transfer(msg.sender, outcomeTokenCount));
        // Add outcome token count to market maker net balance
        require(int(outcomeTokenCount) >= 0);
        netOutcomeTokensSold[outcomeTokenIndex] = netOutcomeTokensSold[outcomeTokenIndex].add(int(outcomeTokenCount));
        OutcomeTokenPurchase(msg.sender, outcomeTokenIndex, outcomeTokenCount, outcomeTokenCost, fees);
    }

    /// @dev Allows to sell outcome tokens to market maker
    /// @param outcomeTokenIndex Index of the outcome token to sell
    /// @param outcomeTokenCount Amount of outcome tokens to sell
    /// @param minProfit The minimum profit in collateral tokens to earn for outcome tokens
    /// @return Profit in collateral tokens
    function sell(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint minProfit)
        public
        atStage(Stages.MarketFunded)
        returns (uint profit)
    {
        // Calculate profit for selling outcome tokens
        uint outcomeTokenProfit = marketMaker.calcProfit(this, outcomeTokenIndex, outcomeTokenCount);
        // Calculate fee charged by market
        uint fees = calcMarketFee(outcomeTokenProfit);
        profit = outcomeTokenProfit.sub(fees);
        // Check profit is not too low
        require(profit > 0 && profit >= minProfit);
        // Transfer outcome tokens to markets contract to sell all outcomes
        require(eventContract.outcomeTokens(outcomeTokenIndex).transferFrom(msg.sender, this, outcomeTokenCount));
        // Sell all outcomes
        eventContract.sellAllOutcomes(outcomeTokenProfit);
        // Transfer profit to seller
        require(eventContract.collateralToken().transfer(msg.sender, profit));
        // Subtract outcome token count from market maker net balance
        require(int(outcomeTokenCount) >= 0);
        netOutcomeTokensSold[outcomeTokenIndex] = netOutcomeTokensSold[outcomeTokenIndex].sub(int(outcomeTokenCount));
        OutcomeTokenSale(msg.sender, outcomeTokenIndex, outcomeTokenCount, outcomeTokenProfit, fees);
    }

    /// @dev Buys all outcomes, then sells all shares of selected outcome which were bought, keeping
    ///      shares of all other outcome tokens.
    /// @param outcomeTokenIndex Index of the outcome token to short sell
    /// @param outcomeTokenCount Amount of outcome tokens to short sell
    /// @param minProfit The minimum profit in collateral tokens to earn for short sold outcome tokens
    /// @return Cost to short sell outcome in collateral tokens
    function shortSell(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint minProfit)
        public
        returns (uint cost)
    {
        // Buy all outcomes
        require(   eventContract.collateralToken().transferFrom(msg.sender, this, outcomeTokenCount)
                && eventContract.collateralToken().approve(eventContract, outcomeTokenCount));
        eventContract.buyAllOutcomes(outcomeTokenCount);
        // Short sell selected outcome
        eventContract.outcomeTokens(outcomeTokenIndex).approve(this, outcomeTokenCount);
        uint profit = this.sell(outcomeTokenIndex, outcomeTokenCount, minProfit);
        cost = outcomeTokenCount - profit;
        // Transfer outcome tokens to buyer
        uint8 outcomeCount = eventContract.getOutcomeCount();
        for (uint8 i = 0; i < outcomeCount; i++)
            if (i != outcomeTokenIndex)
                require(eventContract.outcomeTokens(i).transfer(msg.sender, outcomeTokenCount));
        // Send change back to buyer
        require(eventContract.collateralToken().transfer(msg.sender, profit));
        OutcomeTokenShortSale(msg.sender, outcomeTokenIndex, outcomeTokenCount, cost);
    }

    /// @dev Calculates fee to be paid to market maker
    /// @param outcomeTokenCost Cost for buying outcome tokens
    /// @return Fee for trade
    function calcMarketFee(uint outcomeTokenCost)
        public
        constant
        returns (uint)
    {
        return outcomeTokenCost * fee / FEE_RANGE;
    }
}
