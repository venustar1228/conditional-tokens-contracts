from ..abstract_test import AbstractTestContract, accounts, keys


class TestContract(AbstractTestContract):
    """
    run test with python -m unittest contracts.tests.market_makers.test_move_price_to_0
    """

    def __init__(self, *args, **kwargs):
        super(TestContract, self).__init__(*args, **kwargs)
        self.math = self.create_contract('Utils/Math.sol')
        self.event_factory = self.create_contract('Events/EventFactory.sol', libraries={'Math': self.math})
        self.centralized_oracle_factory = self.create_contract('Oracles/CentralizedOracleFactory.sol')
        self.market_factory = self.create_contract('Markets/DefaultMarketFactory.sol')
        self.lmsr = self.create_contract('MarketMakers/LMSRMarketMaker.sol', libraries={'Math': self.math})
        self.ether_token = self.create_contract('Tokens/EtherToken.sol', libraries={'Math': self.math})
        self.token_abi = self.create_abi('Tokens/AbstractToken.sol')
        self.market_abi = self.create_abi('Markets/DefaultMarket.sol')
        self.event_abi = self.create_abi('Events/AbstractEvent.sol')

    def test(self):
        # Create event
        description_hash = "d621d969951b20c5cf2008cbfc282a2d496ddfe75a76afe7b6b32f1470b8a449".decode('hex')
        oracle_address = self.centralized_oracle_factory.createCentralizedOracle(description_hash)
        event = self.contract_at(self.event_factory.createCategoricalEvent(self.ether_token.address, oracle_address, 2), self.event_abi)
        # Create market
        fee = 0  # 0%
        market = self.contract_at(self.market_factory.createMarket(event.address, self.lmsr.address, fee), self.market_abi)
        # Fund market
        investor = 0
        funding = 10*10**18
        self.ether_token.deposit(value=funding, sender=keys[investor])
        self.assertEqual(self.ether_token.balanceOf(accounts[investor]), funding)
        self.ether_token.approve(market.address, funding, sender=keys[investor])
        market.fund(funding, sender=keys[investor])
        self.assertEqual(self.ether_token.balanceOf(accounts[investor]), 0)
        # User buys all outcomes
        trader = 1
        outcome = 1
        token_count = 100 * 10 ** 18  # 100 Ether
        loop_count = 10
        self.ether_token.deposit(value=token_count * loop_count, sender=keys[trader])
        self.ether_token.approve(event.address, token_count * loop_count, sender=keys[trader])
        event.buyAllOutcomes(token_count * loop_count, sender=keys[trader])
        # User sells tokens
        buyer_balance = self.ether_token.balanceOf(accounts[trader])
        profits = None
        for i in range(loop_count):
            # Calculate profit for selling tokens
            profits = self.lmsr.calcProfits(market.address, outcome, token_count)
            if profits == 0:
                break
            # Selling tokens
            outcome_token = self.contract_at(event.outcomeTokens(outcome), self.token_abi)
            outcome_token.approve(market.address, token_count, sender=keys[trader])
            self.assertEqual(market.sell(outcome, token_count, profits, sender=keys[trader]), profits)
        # Selling of tokens is worth less than 1 Wei
        self.assertEqual(profits, 0)
        # User's Ether balance increased
        self.assertGreater(self.ether_token.balanceOf(accounts[trader]), buyer_balance)
