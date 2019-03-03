import pytest
from hanziconv import HanziConv


convert = HanziConv.toSimplified


def test_convert_custom_mapping():
    custom_mapping = {
        '祢': '祢',
        '面': '面',
        '里': '裡',
        '傢': '家',
    }

    text = '住在祢傢里面'
    expected = '住在祢家裡面'

    assert convert(text, custom_mapping=custom_mapping) == expected
