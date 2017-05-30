Gnosis Smart Contracts Documentation
====================================

<img src="assets/class_diagram.png" />

Introduction
------------
The Gnosis smart contract design follows a modular contract structure making it easy to split functionalities to upgrade or reuse parts. The current Gnosis implementation consists of over 25 smart contracts ranging from different oracle solutions to market makers. All of them have been written in Solidity.

For every prediction market two main objects have to be created:
1. An event object referencing an oracle to resolve the event and a collateral token to exchange outcome tokens for collateral tokens.
2. A market object, which connects a market maker with the event.

Once the event occurred, the event can be resolved and winnings can be redeemed.


Events
------
### Abstract event
The abstract event contract contains all contract functionality shared between scalar and categorical events.

#### Event(Token _collateralToken, Oracle _oracle, uint8 outcomeCount)
On a event creation a collateral token, an oracle and an outcome count have to be defined. The collateral token is used to deposit a collateral in return for outcome tokens. A common collateral token is Ether itself. The oracle is used to define which outcome was resolved as the winning outcome. The outcome count defines the number of outcome tokens. One outcome token is created for each outcome when the event is created.

#### buyAllOutcomes(uint collateralTokenCount)
`buyAllOutcomes` allows to buy multiple sets of outcome tokens in exchange for multiple (`collateralTokenCount`) collateral tokens. Assuming an event has two outcomes and the buyer invests 10 collateral tokens, he will receive 10 outcome tokens for each outcome.

#### sellAllOutcomes(uint outcomeTokenCount)
`sellAllOutcomes` allows to sell multiple (`outcomeTokenCount`) sets of outcome tokens in exchange for multiple collateral tokens. Assuming an event has two outcomes and the buyer sells 2 sets of outcome tokens (2 outcome tokens for each outcome), he will receive 2 collateral tokens.

#### setWinningOutcome()
`setWinningOutcome` sets the winning outcome in the event contract if the defined oracle contract set a winning outcome.

#### redeemWinnings() returns (uint)
Abstract function implemented in the inheriting event contract.

#### getOutcomeCount() returns (uint8)
Returns the number of event outcomes.

#### getOutcomeTokens() returns (OutcomeToken[])
Returns the addresses of all event outcome tokens.

#### getOutcomeTokenDistribution(address owner) returns (uint[] outcomeTokenDistribution)
Returns an array of outcome tokens balances for an `owner`.

#### getEventHash() returns (bytes32)
Abstract function implemented in the inheriting event contract.

### Categorical event
Categorical events define a set of outcomes and resolve to one outcome out of this set of outcomes. An example for such an event is an election where the set of outcomes is defined as the set of candidates participating in the election:

Event: Who becomes the next president of the United States?

Outcomes: Donald Trump, Hilary Clinton.

The set of outcomes has to cover all possible outcomes. The probability of all outcomes has to add up to 100%.

Using the `buyAllOutcomes` function a buyer can invest collateral tokens in return for a set of outcome tokens:

<img src="assets/categorical_event_buy.png" />

Using the `sellAllOutcomes` function a seller can sell a set of outcome tokens for collateral tokens:

<img src="assets/categorical_event_sell.png" />

After the oracle decided the winning outcome, one winning outcome token can be redeemed for one collateral token. All other outcome tokens are worthless.

#### CategoricalEvent(Token _collateralToken, Oracle _oracle, uint8 outcomeCount)
An categorical event has the same properties as the abstract event contract. Only one event for each combination of properties (collateral token, oracle, outcome count) can be created. This allows to combine liquidity for each currency and outcome in only one event. Several markets can use the same event to share this liquidity pool.

#### redeemWinnings() returns (uint)
Redeem winnings allows the sender to redeem winning outcome tokens for collateral tokens. The function revokes all sender's outcome tokens of the winning outcome and sends the same amount in collateral tokens back to the sender. The function returns this amount.

#### getEventHash() returns (bytes32)
This function generates a unique event hash based on the event properties: collateral token, oracle and outcome count.

### Scalar event
Scalar events are used to predict a number within a defined range. An example for such an event is the prediction of a future price:

Event: What will be the Apple Inc. stock price per share be at the end of 2017?

Range: $300 - $1000

For every scalar event two outcome tokens are created. One outcome token for long positions and one for short positions.

Using the `buyAllOutcomes` function a buyer can invest collateral tokens in return for long and short outcome tokens:

<img src="assets/scalar_event_buy.png" />

Using the `sellAllOutcomes` function a seller can sell sets of long and one short outcome tokens for collateral tokens:

<img src="assets/scalar_event_sell.png" />

#### ScalarEvent(Token _collateralToken, Oracle _oracle, int _lowerBound, int _upperBound)
A scalar event has the same properties as the abstract event contract and extends the model with a lower and an upper bound. Scalar events have always only 2 outcome tokens for long and short positions. Only one event for each combination of properties (collateral token, oracle, lower bound, upper bound) can be created. This allows to combine liquidity for each currency, oracle and range in only one event. Several markets can use the same event to share this liquidity pool.

#### redeemWinnings() returns (uint)
Redeem winnings allows the sender to redeem outcome tokens for collateral tokens. The function revokes all sender's outcome tokens and sends the winnings as collateral tokens back to the sender. The function returns the amount of collateral tokens.

The following graph shows how payouts are done in scalar events:

<img src="assets/scalar_event_payout.png" />

If the resolved outcome is below the lower bound, long outcome tokens have no value and short outcome tokens have the value of 1 unit of collateral tokens.

If the resolved outcome is within the lower and upper bound, the value of short outcome tokens decreases linearly and the value of long outcome tokens increases linearly the higher the outcome in the range is.

If the resolved outcome is higher than the upper bound, long outcome tokens have the value of 1 unit of collateral tokens and short outcome tokens have no value.

Regardless off the resolved value, the sum of payoff of any complete set is always 1 unit of collateral tokens.

#### getEventHash() returns (bytes32)
This function generates a unique event hash based on the event properties: collateral token, oracle, outcome count, lower bound and upper bound.

Outcome tokens
--------------
Outcome tokens are ERC20 compatible and can be used as collateral tokens for other events. The interesting feature of outcome tokens is, that they only have a value when the outcome they represent occurred. Trading an event using an outcome token as collateral implies that the event is only relevant under the assumption that the outcome occurred. This allows to create events with conditional probabilities.

Assuming we want to predict, how the potential change of the Microsoft CEO affects the Microsoft stock price, we create two events:

1. Will Steve Ballmer be CEO of Microsoft end of 2014? Outcomes: Yes, No
2. What is Microsoft stock price end of 2014? Outcome: Any number

The first event can use Ether as collateral token but for the second market, we use the No outcome token representing the outcome "Steve Ballmer is not CEO of Microsoft end of 2014". Any market using the second event is predicting the stock price of Microsoft end 2014 under the assumption that Steve Ballmer is no longer CEO end 2017.

Oracles
-------
The Gnosis platform is agnostic towards oracle solutions. Any smart contract implementing the oracle interface can be used as an oracle to resolve events. Our smart contracts already include many different oracle solutions for different use cases. We differentiate between regular oracles and proxy oracles. Proxy oracles cannot function as standalone oracles but have to define other oracles, which they utilize for resolution. One example is the majority oracle, which requires other oracles to come to a majority decision to resolve an event. All oracles have in common that the outcome can only be set once.

<img src="assets/oracles.png" />

### Abstract oracle
The abstract oracle contract contains all functions, which have to be implemented by all oracles.

#### isOutcomeSet() returns (bool)
Returns if the outcome was resolved yet.

#### getOutcome() returns (int)
Returns the outcome as a signed integer. In case of categorical event, the outcome is the index of the winning outcome token. If the first outcome won, the winning outcome is 0. In case of a scalar event, the result will be the winning number.

### Centralized oracle
The centralized oracle is the simplest oracle. The owner creates a new centralized oracle contract and can set the outcome afterwards by sending a transaction.

#### CentralizedOracle(address _owner, bytes32 _descriptionHash)
The owner address is set to the sender address by the factory contract. The description hash is provided by the sender creating the oracle referencing a hashed event description.

#### replaceOwner(address _owner)
The replace owner function allows the oracle owner to exchange the owner address, allowing another ethereum account to define the outcome. This is only possible before an outcome was set. The reason for this function is the option to replace an account with a more protected account in case the relevance of an oracle is increasing because the markets depending on the oracle increase in volume.

#### setOutcome(int _outcome)
Allows the contract owner ot set the outcome. The outcome can only be set once.

### Difficulty oracle
The difficulty oracle allows to resolve an event based on the difficulty after a specified block.

#### DifficultyOracle(uint _blockNumber)
The oracle creator creates an difficulty oracle by defining the block number after which the difficulty should be set as the outcome.

#### setOutcome()
Allows to set the outcome if the defined block number was reached.

### Majority oracle
The majority oracle is a proxy oracle resolving to the outcome defined by an absolute majority of defined oracles. Assuming there are 5 defined oracles, 3 of them have to set the same outcome to resolve the majority oracle. The majority oracle cannot be resolved in standoff situations. This is why this oracle should always be used with a backstop oracle like the ultimate oracle.

#### MajorityOracle(Oracle[] _oracles)
When a majority oracle is created, at least 3 oracles have to be defined. The oracle addresses are saved in the majority oracle contract.

#### getStatusAndOutcome() returns (bool outcomeSet, int outcome)
This function returns if the majority oracle was resolved and the resolved outcome. In case the oracle was not resolved yet, the outcome value is 0.

### Signed message oracle
Signed message oracles allow to set an oracle based on a signed message. The Ethereum account accepted as signer is defined at oracle creation. The advantage over the centralized oracle is, that the oracle contract creator and the outcome signer don't have ot be the same entity but a third party like Reality Keys can be used to sign outcomes.

#### SignedMessageOracle(bytes32 _descriptionHash, uint8 v, bytes32 r, bytes32 s)
When a signed message oracle is created an event description hash and the signer's signature of the description hash are sent. The allowed outcome signer is derived from the description hash and the given signature and saved in the oracle contract.

#### replaceSigner(address _signer, uint _nonce, uint8 v, bytes32 r, bytes32 s)
Similarly to the centralized oracle, the account allowed to set the outcome can be replaced by the currently allowed account. This is useful if the private key allowed to sign the outcome should be replaced with another one with higher protection in case markets resolved by this event become very popular. The new signer address, a nonce and the current singer's signature are provided. A nonce is required to prevent replay attacks in case multiple substitutions of signers are necessary.

#### setOutcome(int _outcome, uint8 v, bytes32 r, bytes32 s)
Validates that the outcome was signed by the allowed signer and sets the outcome. Once the outcome was set, it cannot be changed anymore.

### Ultimate oracle
The ultimate oracle is a proxy oracle forwarding the result of a predefined oracle. This result can be overwritten by the ultimate oracle in case someone is challenging the outcome. In that sense the ultimate oracle is a backstop oracle used in case the forwarded oracle is acting maliciously. The ultimate oracle is a decentralized oracle, meaning that not a single entity can define the outcome but there has to be consensus within a group of entities about the outcome to resolve the oracle.

<img src="assets/ultimate_oracle.png" />

To challenge an outcome and start the ultimate oracle a user has to put a challenge amount of collateral tokens on the outcome that he believes to be the correct outcome. After the outcome was challenged anyone can put collateral tokens on their preferred outcome. If the outcome with the biggest betting amount (front runner) doesn't change within a defined period, the oracle is resolved and the current front runner is set as the final outcome. To make sure that the spread between the total amount bet and the front runner is not too high so others can catch up, a spread multiplier is defined limiting the spread. After an outcome is decided, the total betting amount is distributed among everyone who put money on the front runner proportionally to their contribution to the front runner.

#### UltimateOracle(Oracle _oracle, Token _collateralToken, uint8 _spreadMultiplier, uint _challengePeriod, uint _challengeAmount, uint _frontRunnerPeriod)
To create an ultimate oracle contract a few settings have to be defined:
1. The forwarded oracle, whose outcome is used in case there is no challenge.
2. The used collateral token to contribute to the ultimate oracle outcome.
3. The spread multiplier to define the max. spread between total betting amounts and front runner.
4. The challenge period in seconds to define how long users have the option to challenge a forwarded outcome before it is set as final.
5. The challenge amount required to challenge an outcome.
6. The front runner period in seconds to define how long a front runner must be leading before the front runner is set as final outcome.

#### setOutcome()
Allows to set the outcome based on the forwarded outcome. It can only be set in case it was set in the forwarded oracle and no challenge was started yet.

#### challengeOutcome(int _outcome)
Allows to challenge the outcome set by the forwarded outcome. The challenge can be started even if no outcome was set yet. The sender has to pay the defined challenge amount in collateral tokens to start the challenge. The amount is bet on the outcome defined by the sender.

#### voteForOutcome(int _outcome, uint amount)
After

#### withdraw() returns (uint amount)
The function allows the sender to withdraw his share in collateral tokens after the final outcome was set.

#### isChallengePeriodOver()
Returns if forwarded outcome was set and the challenge period is over.

#### isFrontRunnerPeriodOver()
Returns if the outcome was challenged and the front runner period is over.

#### isChallenged()
Returns if the outcome was challenged.

Markets
-------
### Abstract market
#### fund(uint _funding)
#### close()
#### withdrawFees()
#### buy(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint maxCosts) returns (uint)
#### sell(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint minProfits) returns (uint)
#### shortSell(uint8 outcomeTokenIndex, uint outcomeTokenCount, uint minProfits) returns (uint)
#### calcMarketFee(uint outcomeTokenCosts) returns (uint)

### Default market
#### DefaultMarket(address _creator, Event _eventContract, MarketMaker _marketMaker, uint _fee)

### Abstract market maker
#### calcCost(Market market, uint8 outcomeTokenIndex, uint outcomeTokenCount) returns (uint)
#### calcProfit(Market market, uint8 outcomeTokenIndex, uint outcomeTokenCount) returns (uint)

### LMSR market maker
