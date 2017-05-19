from ..abstract_test import AbstractTestContract, accounts, keys


class TestContract(AbstractTestContract):
    """
    run test with python -m unittest contracts.tests.events.test_redeem_winnings_for_categorical_event
    """

    def __init__(self, *args, **kwargs):
        super(TestContract, self).__init__(*args, **kwargs)
        self.math = self.create_contract('Utils/Math.sol')
        self.event_factory = self.create_contract('Events/EventFactory.sol', libraries={'Math': self.math})
        self.centralized_oracle_factory = self.create_contract('Oracles/CentralizedOracleFactory.sol')
        self.ether_token = self.create_contract('Tokens/EtherToken.sol', libraries={'Math': self.math})
        self.event_abi = self.create_abi('Events/CategoricalEvent.sol')
        self.token_abi = self.create_abi('Tokens/AbstractToken.sol')
        self.oracle_abi = self.create_abi('Oracles/CentralizedOracle.sol')

    def test(self):
        # Create event
        description_hash = "d621d969951b20c5cf2008cbfc282a2d496ddfe75a76afe7b6b32f1470b8a449".decode('hex')
        oracle_address = self.centralized_oracle_factory.createCentralizedOracle(description_hash)
        event_address = self.event_factory.createCategoricalEvent(self.ether_token.address, oracle_address, 2)
        event = self.contract_at(event_address, self.event_abi)
        oracle = self.contract_at(oracle_address, self.oracle_abi)
        # Get ether tokens
        buyer = 0
        collateral_token_count = 10
        self.ether_token.deposit(value=collateral_token_count, sender=keys[buyer])
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), collateral_token_count)
        # Buy all outcomes
        self.ether_token.approve(event_address, collateral_token_count, sender=keys[buyer])
        event.buyAllOutcomes(collateral_token_count, sender=keys[buyer])
        self.assertEqual(self.ether_token.balanceOf(event_address), collateral_token_count)
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), 0)
        outcome_token_1 = self.contract_at(event.outcomeTokens(0), self.token_abi)
        outcome_token_2 = self.contract_at(event.outcomeTokens(1), self.token_abi)
        self.assertEqual(outcome_token_1.balanceOf(accounts[buyer]), collateral_token_count)
        self.assertEqual(outcome_token_2.balanceOf(accounts[buyer]), collateral_token_count)
        # Set outcome in oracle contract
        oracle.setOutcome(1)
        self.assertEqual(oracle.getOutcome(), 1)
        self.assertTrue(oracle.isOutcomeSet())
        # Set outcome in event
        event.setWinningOutcome()
        self.assertEqual(event.winningOutcome(), 1)
        self.assertTrue(event.isWinningOutcomeSet())
        # Redeem winnings
        self.assertEqual(event.redeemWinnings(sender=keys[buyer]), collateral_token_count)
        self.assertEqual(outcome_token_1.balanceOf(accounts[buyer]), collateral_token_count)
        self.assertEqual(outcome_token_2.balanceOf(accounts[buyer]), 0)
        self.assertEqual(self.ether_token.balanceOf(accounts[buyer]), collateral_token_count)
