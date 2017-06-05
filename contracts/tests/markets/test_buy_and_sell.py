from ..abstract_test import AbstractTestContracts, accounts, keys


class TestContracts(AbstractTestContracts):

    def __init__(self, *args, **kwargs):
        super(TestContracts, self).__init__(*args, **kwargs)
        self.math = self.create_contract('Utils/Math.sol')
        self.event_factory = self.create_contract('Events/EventFactory.sol', libraries={'Math': self.math})
        self.centralized_oracle_factory = self.create_contract('Oracles/CentralizedOracleFactory.sol')
        self.market_factory = self.create_contract('Markets/StandardMarketFactory.sol', libraries={'Math': self.math})
        self.lmsr = self.create_contract('MarketMakers/LMSRMarketMaker.sol', libraries={'Math': self.math})
        self.ether_token = self.create_contract('Tokens/EtherToken.sol', libraries={'Math': self.math})
        self.token_abi = self.create_abi('Tokens/AbstractToken.sol')
        self.market_abi = self.create_abi('Markets/StandardMarket.sol')
        self.event_abi = self.create_abi('Events/AbstractEvent.sol')

    def test(self):
        # Create event
        ipfs_hash = b'QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG'
        oracle_address = self.centralized_oracle_factory.createCentralizedOracle(ipfs_hash)
        event = self.contract_at(self.event_factory.createCategoricalEvent(self.ether_token.address, oracle_address, 2), self.event_abi)
        # Create market
        fee = 50000  # 5%
        market = self.contract_at(self.market_factory.createMarket(event.address, self.lmsr.address, fee), self.market_abi)
        # Fund market
        investor = 0
        funding = 10**18
        self.ether_token.deposit(value=funding, sender=keys[investor])
        self.assertEqual(self.ether_token.balanceOf(accounts[investor]), funding)
        self.ether_token.approve(market.address, funding, sender=keys[investor])
        market.fund(funding, sender=keys[investor])
        self.assertEqual(self.ether_token.balanceOf(accounts[investor]), 0)
        # Buy outcome tokens
        buyer = 1
        outcome = 0
        token_count = 10**15
        outcome_token_cost = self.lmsr.calcCost(market.address, outcome, token_count)
        fee = market.calcMarketFee(outcome_token_cost)
        self.assertEqual(fee, outcome_token_cost * 105 // 100 - outcome_token_cost)
        cost = outcome_token_cost + fee
        self.ether_token.deposit(value=cost, sender=keys[buyer])
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), cost)
        self.ether_token.approve(market.address, cost, sender=keys[buyer])
        self.assertEqual(market.buy(outcome, token_count, cost, sender=keys[buyer]), cost)
        outcome_token = self.contract_at(event.outcomeTokens(outcome), self.token_abi)
        self.assertEqual(outcome_token.balanceOf(accounts[buyer]), token_count)
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), 0)
        # Sell outcome tokens
        outcome_token_profit = self.lmsr.calcProfit(market.address, outcome, token_count)
        fee = market.calcMarketFee(outcome_token_profit)
        profit = outcome_token_profit - fee
        outcome_token.approve(market.address, token_count, sender=keys[buyer])
        self.assertEqual(market.sell(outcome, token_count, profit, sender=keys[buyer]), profit)
        self.assertEqual(outcome_token.balanceOf(accounts[buyer]), 0)
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), profit)
