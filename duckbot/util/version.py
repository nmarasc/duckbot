# -*- coding: utf-8 -*-
"""Collection of functions to return PEP 440 valid version info."""
from typing import Tuple


def getVersion(version: Tuple[int, int, int, str, int]) -> str:
    """Convert version tuple into PEP 440 compliant string.

    Parameters
    ----------
    version
        Version information

    Returns
    -------
    str
        PEP 440 compliant version string, X.Y.Z[{a|b|rc}N]

        a, b, rc for alpha, beta, release contender

        e.g. 1.2.3rc4

    Raises
    ------
    AssertionError
        The fourth value in the version tuple was not a valid string

        Valid strings are 'alpha', 'beta', 'rc', 'final'
    """
    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Main version is always of the form X.Y.Z
    main = '.'.join(str(x) for x in version[:3])

    sub = ''
    if version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub
