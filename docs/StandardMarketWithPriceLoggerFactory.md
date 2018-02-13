* [StandardMarketWithPriceLoggerFactory](#standardmarketwithpriceloggerfactory)
  * [Accessors](#standardmarketwithpriceloggerfactory-accessors)
  * [Events](#standardmarketwithpriceloggerfactory-events)
    * [StandardMarketWithPriceLoggerCreation(*address* indexed `creator`, *address* `market`, *address* `eventContract`, *address* `marketMaker`, *uint24* `fee`, *uint256* `startDate`)](#standardmarketwithpriceloggercreationaddress-indexed-creator-address-market-address-eventcontract-address-marketmaker-uint24-fee-uint256-startdate)
  * [Functions](#standardmarketwithpriceloggerfactory-functions)
    * [createMarket(*address* `eventContract`, *address* `marketMaker`, *uint24* `fee`, *uint256* `startDate`)](#createmarketaddress-eventcontract-address-marketmaker-uint24-fee-uint256-startdate)

# StandardMarketWithPriceLoggerFactory

### Market factory contract - Allows to create market contracts

- **Author**: Stefan George - <stefan@gnosis.pm>
- **Constructor**: StandardMarketWithPriceLoggerFactory(*address* `_standardMarketWithPriceLoggerMasterCopy`)
- This contract does **not** have a fallback function.

## StandardMarketWithPriceLoggerFactory Accessors

* *address* standardMarketWithPriceLoggerMasterCopy() `d8218744`

## StandardMarketWithPriceLoggerFactory Events

### StandardMarketWithPriceLoggerCreation(*address* indexed `creator`, *address* `market`, *address* `eventContract`, *address* `marketMaker`, *uint24* `fee`, *uint256* `startDate`)

**Signature hash**: `969b1ad77db8ae8298dedcdf1f2945322eaf681e1d56fcebfd4c23de996dc484`

## StandardMarketWithPriceLoggerFactory Functions

### createMarket(*address* `eventContract`, *address* `marketMaker`, *uint24* `fee`, *uint256* `startDate`)

- **State mutability**: `nonpayable`
- **Signature hash**: `8e44df53`

Creates a new market contract

#### Inputs

| type      | name            | description                  |
| --------- | --------------- | ---------------------------- |
| *address* | `eventContract` | Event contract               |
| *address* | `marketMaker`   | Market maker contract        |
| *uint24*  | `fee`           | Market fee                   |
| *uint256* | `startDate`     | Start date for price logging |

#### Outputs

| type      | name     | description     |
| --------- | -------- | --------------- |
| *address* | `market` | Market contract |
