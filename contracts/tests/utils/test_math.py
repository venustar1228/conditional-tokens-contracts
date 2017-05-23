from itertools import chain
from functools import partial

import math
import random

from mpmath import mp
mp.dps = 100

from ethereum.tester import TransactionFailed

from ..abstract_test import AbstractTestContract

if hasattr(math, 'isclose'):
    isclose = math.isclose
else:
    # PEP 485
    def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class TestContract(AbstractTestContract):
    """
    run test with python -m unittest contracts.tests.utils.test_math
    """

    def __init__(self, *args, **kwargs):
        super(TestContract, self).__init__(*args, **kwargs)
        self.math = self.create_contract('Utils/Math.sol')

    def test(self):
        ONE = 0x10000000000000000
        RELATIVE_TOLERANCE = 1e-9

        # int(mp.floor(mp.log((2**256 - 1) / ONE) * ONE))
        MAX_POWER = 2454971259878909886679

        # LN
        self.assertRaises(TransactionFailed, partial(self.math.ln, 0))
        for x in chain(
            (1, ONE, 2**256-1),
            (random.randrange(1, ONE) for _ in range(100)),
            (random.randrange(ONE, 2**256) for _ in range(100)),
        ):
            X, actual, expected = x / ONE, self.math.ln(x) / ONE, mp.log(x / ONE)
            assert X is not None and isclose(actual, expected, rel_tol=RELATIVE_TOLERANCE)

        # EXP
        for x in chain(
            (0, MAX_POWER),
            (random.randrange(MAX_POWER) for _ in range(10)),
        ):
            X, actual, expected = x / ONE, self.math.exp(x) / ONE, mp.exp(x / ONE)
            assert X is not None and isclose(actual, expected, rel_tol=RELATIVE_TOLERANCE)

        # Safe to add
        self.assertFalse(self.math.safeToAdd(2**256 - 1, 1))
        self.assertTrue(self.math.safeToAdd(1, 1))

        # Safe to subtract
        self.assertFalse(self.math.safeToSubtract(1, 2))
        self.assertTrue(self.math.safeToSubtract(1, 1))
