from ..abstract_test import AbstractTestContract, accounts, keys, TransactionFailed
from ethereum import tester as t


class TestContract(AbstractTestContract):
    """
    run test with python -m unittest contracts.tests.oracles.test_futarchy_oracle
    """

    def __init__(self, *args, **kwargs):
        super(TestContract, self).__init__(*args, **kwargs)
        self.math = self.create_contract('Utils/Math.sol')
        self.event_factory = self.create_contract('Events/EventFactory.sol', libraries={'Math': self.math})
        self.centralized_oracle_factory = self.create_contract('Oracles/CentralizedOracleFactory.sol')
        self.market_factory = self.create_contract('Markets/DefaultMarketFactory.sol')
        self.futarchy_factory = self.create_contract('Oracles/FutarchyOracleFactory.sol', params=[self.event_factory])
        self.lmsr = self.create_contract('MarketMakers/LMSRMarketMaker.sol', libraries={'Math': self.math})
        self.ether_token = self.create_contract('Tokens/EtherToken.sol', libraries={'Math': self.math})
        self.token_abi = self.create_abi('Tokens/AbstractToken.sol')
        self.market_abi = self.create_abi('Markets/DefaultMarket.sol')
        self.event_abi = self.create_abi('Events/AbstractEvent.sol')
        self.oracle_abi = self.create_abi('Oracles/CentralizedOracle.sol')
        self.futarchy_abi = self.create_abi('Oracles/FutarchyOracle.sol')

    def test(self):
        t.gas_limit = 4712388*4  # Creation gas costs are above gas limit!!!
        # Create futarchy oracle
        description_hash = "d621d969951b20c5cf2008cbfc282a2d496ddfe75a76afe7b6b32f1470b8a449".decode('hex')
        oracle = self.contract_at(self.centralized_oracle_factory.createCentralizedOracle(description_hash), self.oracle_abi)
        fee = 50000  # 5%
        lower = -100
        upper = 100
        deadline = self.s.block.timestamp + 60*60  # in 1h
        creator = 0
        profiling = self.futarchy_factory.createFutarchyOracle(self.ether_token.address, oracle.address, 2, lower, upper,
                                                               self.market_factory.address, self.lmsr.address, fee,
                                                               deadline, sender=keys[creator], profiling=True)
        self.assertLess(profiling['gas'], 10000000)
        futarchy = self.contract_at(profiling['output'], self.futarchy_abi)
        categorical_event = self.contract_at(futarchy.categoricalEvent(), self.event_abi)
        # Fund markets
        collateral_token_count = 10**18
        self.ether_token.deposit(value=collateral_token_count, sender=keys[creator])
        self.assertEqual(self.ether_token.balanceOf(accounts[creator]), collateral_token_count)
        self.ether_token.approve(futarchy.address, collateral_token_count, sender=keys[creator])
        futarchy.fund(collateral_token_count, sender=keys[creator])
        # Buy into market for outcome token 1
        market = self.contract_at(futarchy.markets(1), self.market_abi)
        buyer = 1
        outcome = 0
        token_count = 10 ** 15
        outcome_token_costs = self.lmsr.calcCosts(market.address, outcome, token_count)
        fee = market.calcMarketFee(outcome_token_costs)
        costs = outcome_token_costs + fee
        # Buy all outcomes
        self.ether_token.deposit(value=costs, sender=keys[buyer])
        self.ether_token.approve(categorical_event.address, costs, sender=keys[buyer])
        categorical_event.buyAllOutcomes(costs, sender=keys[buyer])
        collateral_token = self.contract_at(categorical_event.outcomeTokens(1), self.token_abi)
        collateral_token.approve(market.address, costs, sender=keys[buyer])
        self.assertEqual(market.buy(outcome, token_count, costs, sender=keys[buyer]), costs)
        # Set outcome of futarchy oracle
        self.assertRaises(TransactionFailed, futarchy.setOutcome)
        self.s.block.timestamp = deadline
        futarchy.setOutcome()
        self.assertTrue(futarchy.isOutcomeSet())
        self.assertEqual(futarchy.getOutcome(), 1)
        categorical_event.setWinningOutcome()
        # Set winning outcome for scalar events
        self.assertRaises(TransactionFailed, futarchy.close)
        oracle.setOutcome(50)
        scalar_event = self.contract_at(market.eventContract(), self.event_abi)
        scalar_event.setWinningOutcome()
        # Close winning market and transfer collateral tokens to creator
        futarchy.close(sender=keys[creator])
        self.assertGreater(self.ether_token.balanceOf(accounts[creator]), collateral_token_count)
