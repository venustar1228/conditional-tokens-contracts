* [ScalarEvent](#scalarevent)
  * [Accessors](#scalarevent-accessors)
  * [Events](#scalarevent-events)
    * [OutcomeTokenCreation(*address* `outcomeToken`, *uint8* `index`)](#outcometokencreationaddress-outcometoken-uint8-index)
    * [OutcomeTokenSetIssuance(*address* indexed `buyer`, *uint256* `collateralTokenCount`)](#outcometokensetissuanceaddress-indexed-buyer-uint256-collateraltokencount)
    * [OutcomeTokenSetRevocation(*address* indexed `seller`, *uint256* `outcomeTokenCount`)](#outcometokensetrevocationaddress-indexed-seller-uint256-outcometokencount)
    * [OutcomeAssignment(*int256* `outcome`)](#outcomeassignmentint256-outcome)
    * [WinningsRedemption(*address* indexed `receiver`, *uint256* `winnings`)](#winningsredemptionaddress-indexed-receiver-uint256-winnings)
  * [Functions](#scalarevent-functions)
    * [setOutcome()](#setoutcome)
    * [buyAllOutcomes(*uint256* `collateralTokenCount`)](#buyalloutcomesuint256-collateraltokencount)
    * [getOutcomeTokenDistribution(*address* `owner`)](#getoutcometokendistributionaddress-owner)
    * [sellAllOutcomes(*uint256* `outcomeTokenCount`)](#sellalloutcomesuint256-outcometokencount)
    * [getOutcomeCount()](#getoutcomecount)
    * [redeemWinnings()](#redeemwinnings)
    * [getEventHash()](#geteventhash)
    * [getOutcomeTokens()](#getoutcometokens)
* [ScalarEventData](#scalareventdata)
  * [Accessors](#scalareventdata-accessors)
* [ScalarEventProxy](#scalareventproxy)
  * [Accessors](#scalareventproxy-accessors)
  * [Events](#scalareventproxy-events)
    * [OutcomeTokenCreation(*address* `outcomeToken`, *uint8* `index`)](#outcometokencreationaddress-outcometoken-uint8-index)
    * [OutcomeTokenSetIssuance(*address* indexed `buyer`, *uint256* `collateralTokenCount`)](#outcometokensetissuanceaddress-indexed-buyer-uint256-collateraltokencount)
    * [OutcomeTokenSetRevocation(*address* indexed `seller`, *uint256* `outcomeTokenCount`)](#outcometokensetrevocationaddress-indexed-seller-uint256-outcometokencount)
    * [OutcomeAssignment(*int256* `outcome`)](#outcomeassignmentint256-outcome)
    * [WinningsRedemption(*address* indexed `receiver`, *uint256* `winnings`)](#winningsredemptionaddress-indexed-receiver-uint256-winnings)

# ScalarEvent

### Scalar event contract - Scalar events resolve to a number within a range

- **Author**: Stefan George - <stefan@gnosis.pm>
- **Constructor**: ScalarEvent()
- This contract does **not** have a fallback function.

## ScalarEvent Accessors

* *int256* outcome() `27793f87`
* *uint8* LONG() `561cce0a`
* *uint24* OUTCOME_RANGE() `6e5452fe`
* *address* oracle() `7dc0d1d0`
* *address* outcomeTokens(*uint256*) `8abe59ea`
* *int256* lowerBound() `a384d6ff`
* *address* masterCopy() `a619486e`
* *uint8* SHORT() `a871da91`
* *int256* upperBound() `b09ad8a0`
* *address* collateralToken() `b2016bd4`
* *bool* isOutcomeSet() `ccdf68f3`

## ScalarEvent Events

### OutcomeTokenCreation(*address* `outcomeToken`, *uint8* `index`)

**Signature hash**: `ad24776dc347085865b6988e249c191fc22d9b31cf54cb62233c3c16be1736ee`

### OutcomeTokenSetIssuance(*address* indexed `buyer`, *uint256* `collateralTokenCount`)

**Signature hash**: `ad2a02292986148558019ae4abf172732228e32e131a91d3fa7e0cada61932c0`

### OutcomeTokenSetRevocation(*address* indexed `seller`, *uint256* `outcomeTokenCount`)

**Signature hash**: `7ac9271efd660c24459c447459e46f7366d2b4a692e572f108619d0d7273fcc5`

### OutcomeAssignment(*int256* `outcome`)

**Signature hash**: `b1aaa9f4484acc283375c8e495a44766e4026170797dc9280b4ae2ab5632fb71`

### WinningsRedemption(*address* indexed `receiver`, *uint256* `winnings`)

**Signature hash**: `2fe921bb50a459800ae7eae7c0124e9e875094a539eb7dc5b3f728017347e0fb`

## ScalarEvent Functions

### setOutcome()

- **State mutability**: `nonpayable`
- **Signature hash**: `0537665d`

Sets winning event outcome

### buyAllOutcomes(*uint256* `collateralTokenCount`)

- **State mutability**: `nonpayable`
- **Signature hash**: `28da850b`

Buys equal number of tokens of all outcomes, exchanging collateral tokens and sets of outcome tokens 1:1

#### Inputs

| type      | name                   | description                 |
| --------- | ---------------------- | --------------------------- |
| *uint256* | `collateralTokenCount` | Number of collateral tokens |

### getOutcomeTokenDistribution(*address* `owner`)

- **State mutability**: `view`
- **Signature hash**: `69c19d4c`

Returns the amount of outcome tokens held by owner

#### Inputs

| type      | name    |
| --------- | ------- |
| *address* | `owner` |

#### Outputs

| type        | name                       | description                |
| ----------- | -------------------------- | -------------------------- |
| *uint256[]* | `outcomeTokenDistribution` | Outcome token distribution |

### sellAllOutcomes(*uint256* `outcomeTokenCount`)

- **State mutability**: `nonpayable`
- **Signature hash**: `6fb1edcd`

Sells equal number of tokens of all outcomes, exchanging collateral tokens and sets of outcome tokens 1:1

#### Inputs

| type      | name                | description              |
| --------- | ------------------- | ------------------------ |
| *uint256* | `outcomeTokenCount` | Number of outcome tokens |

### getOutcomeCount()

- **State mutability**: `view`
- **Signature hash**: `7dc8f086`

Returns outcome count

#### Outputs

| type    | description   |
| ------- | ------------- |
| *uint8* | Outcome count |

### redeemWinnings()

- **State mutability**: `nonpayable`
- **Signature hash**: `ad0b2bec`

Exchanges sender's winning outcome tokens for collateral tokens

#### Outputs

| type      | name       | description       |
| --------- | ---------- | ----------------- |
| *uint256* | `winnings` | Sender's winnings |

### getEventHash()

- **State mutability**: `view`
- **Signature hash**: `e96e5950`

Calculates and returns event hash

#### Outputs

| type      | description |
| --------- | ----------- |
| *bytes32* | Event hash  |

### getOutcomeTokens()

- **State mutability**: `view`
- **Signature hash**: `f21a1468`

Returns outcome tokens array

#### Outputs

| type        | description    |
| ----------- | -------------- |
| *address[]* | Outcome tokens |

# ScalarEventData

- **Constructor**: ScalarEventData()
- This contract does **not** have a fallback function.

## ScalarEventData Accessors

* *uint8* LONG() `561cce0a`
* *uint24* OUTCOME_RANGE() `6e5452fe`
* *int256* lowerBound() `a384d6ff`
* *uint8* SHORT() `a871da91`
* *int256* upperBound() `b09ad8a0`

# ScalarEventProxy

- **Constructor**: ScalarEventProxy(*address* `proxied`, *address* `outcomeTokenMasterCopy`, *address* `_collateralToken`, *address* `_oracle`, *int256* `_lowerBound`, *int256* `_upperBound`)
- This contract has a `payable` fallback function.

## ScalarEventProxy Accessors

* *int256* outcome() `27793f87`
* *uint8* LONG() `561cce0a`
* *uint24* OUTCOME_RANGE() `6e5452fe`
* *address* oracle() `7dc0d1d0`
* *address* outcomeTokens(*uint256*) `8abe59ea`
* *int256* lowerBound() `a384d6ff`
* *address* masterCopy() `a619486e`
* *uint8* SHORT() `a871da91`
* *int256* upperBound() `b09ad8a0`
* *address* collateralToken() `b2016bd4`
* *bool* isOutcomeSet() `ccdf68f3`

## ScalarEventProxy Events

### OutcomeTokenCreation(*address* `outcomeToken`, *uint8* `index`)

**Signature hash**: `ad24776dc347085865b6988e249c191fc22d9b31cf54cb62233c3c16be1736ee`

### OutcomeTokenSetIssuance(*address* indexed `buyer`, *uint256* `collateralTokenCount`)

**Signature hash**: `ad2a02292986148558019ae4abf172732228e32e131a91d3fa7e0cada61932c0`

### OutcomeTokenSetRevocation(*address* indexed `seller`, *uint256* `outcomeTokenCount`)

**Signature hash**: `7ac9271efd660c24459c447459e46f7366d2b4a692e572f108619d0d7273fcc5`

### OutcomeAssignment(*int256* `outcome`)

**Signature hash**: `b1aaa9f4484acc283375c8e495a44766e4026170797dc9280b4ae2ab5632fb71`

### WinningsRedemption(*address* indexed `receiver`, *uint256* `winnings`)

**Signature hash**: `2fe921bb50a459800ae7eae7c0124e9e875094a539eb7dc5b3f728017347e0fb`
