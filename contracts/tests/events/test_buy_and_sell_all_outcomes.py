from ..abstract_test import AbstractTestContract, accounts


class TestContract(AbstractTestContract):
    """
    run test with python -m unittest contracts.tests.events.test_buy_and_sell_all_outcomes
    """

    def __init__(self, *args, **kwargs):
        super(TestContract, self).__init__(*args, **kwargs)
        self.math = self.create_contract('Utils/Math.sol')
        self.event_factory = self.create_contract('Events/EventFactory.sol', libraries={'Math': self.math})
        self.centralized_oracle_factory = self.create_contract('Oracles/CentralizedOracleFactory.sol')
        self.ether_token = self.create_contract('Tokens/EtherToken.sol', libraries={'Math': self.math})
        self.event_abi = self.create_abi('Events/AbstractEvent.sol')
        self.token_abi = self.create_abi('Tokens/AbstractToken.sol')

    def test(self):
        # Create event
        description_hash = "d621d969951b20c5cf2008cbfc282a2d496ddfe75a76afe7b6b32f1470b8a449".decode('hex')
        oracle = self.centralized_oracle_factory.createCentralizedOracle(description_hash)
        event_address = self.event_factory.createCategoricalEvent(self.ether_token.address, oracle, 2)
        event = self.contract_at(event_address, self.event_abi)
        # Buy all outcomes
        buyer = 0
        collateral_token_count = 10
        self.ether_token.deposit(value=collateral_token_count)
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), collateral_token_count)
        self.ether_token.approve(event_address, collateral_token_count)
        event.buyAllOutcomes(collateral_token_count)
        self.assertEqual(self.ether_token.balanceOf(event_address), collateral_token_count)
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), 0)
        outcome_token_1 = self.contract_at(event.outcomeTokens(0), self.token_abi)
        outcome_token_2 = self.contract_at(event.outcomeTokens(1), self.token_abi)
        self.assertEqual(outcome_token_1.balanceOf(accounts[buyer]), collateral_token_count)
        self.assertEqual(outcome_token_2.balanceOf(accounts[buyer]), collateral_token_count)
        # Sell all outcomes
        event.sellAllOutcomes(collateral_token_count)
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), collateral_token_count)
        self.assertEqual(self.ether_token.balanceOf(event_address), 0)
        self.assertEqual(outcome_token_1.balanceOf(accounts[buyer]), 0)
        self.assertEqual(outcome_token_2.balanceOf(accounts[buyer]), 0)
