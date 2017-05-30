from itertools import chain
from functools import partial

import math
import random

from mpmath import mp
mp.dps = 100

from ethereum.tester import TransactionFailed

from ..abstract_test import AbstractTestContracts

if hasattr(math, 'isclose'):
    isclose = math.isclose
else:
    # PEP 485
    def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class TestContracts(AbstractTestContracts):

    def __init__(self, *args, **kwargs):
        super(TestContracts, self).__init__(*args, **kwargs)
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
            X, actual, expected = float(x) / ONE, float(self.math.ln(x)) / ONE, mp.log(float(x) / ONE)
            assert X is not None and isclose(actual, expected, rel_tol=RELATIVE_TOLERANCE)

        # EXP
        for x in chain(
            (0, MAX_POWER),
            (random.randrange(MAX_POWER) for _ in range(10)),
        ):
            X, actual, expected = float(x) / ONE, float(self.math.exp(x)) / ONE, mp.exp(float(x) / ONE)
            assert X is not None and isclose(actual, expected, rel_tol=RELATIVE_TOLERANCE)

        # Safe to add
        self.assertFalse(self.math.safeToAdd(2**256 - 1, 1))
        self.assertTrue(self.math.safeToAdd(1, 1))

        # Safe to subtract
        self.assertFalse(self.math.safeToSub(1, 2))
        self.assertTrue(self.math.safeToSub(1, 1))

        # Safe to multiply
        self.assertFalse(self.math.safeToMul(2**128, 2**128))
        self.assertTrue(self.math.safeToMul(2**256/2 - 1, 2))

        # Add
        self.assertRaises(TransactionFailed, self.math.add, 2**256 - 1, 1)
        self.assertEqual(self.math.add(1, 1), 2)

        # Sub
        self.assertRaises(TransactionFailed, self.math.sub, 1, 2)
        self.assertEqual(self.math.sub(1, 1), 0)

        # Mul
        self.assertRaises(TransactionFailed, self.math.mul, 2**128, 2**128)
        self.assertEqual(self.math.mul(5, 5), 25)
