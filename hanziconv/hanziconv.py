# -*- coding: utf-8 -*-
#
# Copyright 2014 Bernard Yue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import unicode_literals

__doc__ = """
Hanzi Converter 繁簡轉換器 | 繁简转换器

This module provides functions converting chinese text between simplified and
traditional characters.  It returns unicode represnetation of the text.

Class HanziConv is the main entry point of the module, you can import the
class by doing:

    >>> from hanziconv import HanziConv
"""

from .charmap import (simplified_charmap,
                      traditional_charmap,
                      simp_to_trad,
                      trad_to_simp)


class HanziConv(object):
    """This class supports hanzi (漢字) convention between simplified and
    traditional format"""
    __traditional_charmap = traditional_charmap
    __simplified_charmap = simplified_charmap

    @classmethod
    def __convert(cls, text, toTraditional=True, custom_mapping=None):
        """Convert `text` to Traditional characters if `toTraditional` is
        True, else convert to simplified characters

        :param text:           data to convert
        :param toTraditional:  True -- convert to traditional text
                               False -- covert to simplified text
        :returns:              converted 'text`
        """
        if isinstance(text, bytes):
            text = text.decode('utf-8')

        mapper = simp_to_trad
        if not toTraditional:
            mapper = trad_to_simp

        if custom_mapping:
            assert isinstance(custom_mapping, dict), \
                'custom_mapping should be a dictionary'
            mapper.update(custom_mapping)

        final = []
        for c in text:
            if c in mapper.keys():
                final.append(mapper[c])
            else:
                final.append(c)
        return ''.join(final)

    @classmethod
    def toSimplified(cls, text, custom_mapping=None):
        """Convert `text` to simplified character string.  Assuming text is
        traditional character string

        :param text:           text to convert
        :param custom_mapping: A dictionary of custom mappings to override
                               hanziconv's defaults.
        :returns:              converted UTF-8 characters

        >>> from hanziconv import HanziConv
        >>> print(HanziConv.toSimplified('繁簡轉換器'))
        繁简转换器
        """
        return cls.__convert(text, toTraditional=False, custom_mapping=custom_mapping)

    @classmethod
    def toTraditional(cls, text, custom_mapping=None):
        """Convert `text` to traditional character string.  Assuming text is
        simplified character string

        :param text:  text to convert
        :returns:     converted UTF-8 characters

        >>> from hanziconv import HanziConv
        >>> print(HanziConv.toTraditional('繁简转换器'))
        繁簡轉換器
        >>> print(HanziConv.toTraditional('祢是我的荣耀', custom_mapping={'祢': '祢'}))
        祢是我的榮耀
        """
        return cls.__convert(text, toTraditional=True, custom_mapping=custom_mapping)

    @classmethod
    def same(cls, text1, text2, custom_mapping=None):
        """Return True if text1 and text2 meant literally the same, False
        otherwise

        :param text1: string to compare to ``text2``
        :param text2: string to compare to ``text1``
        :returns:     **True**  -- ``text1`` and ``text2`` are the same in \
            meaning,
                      **False** -- otherwise

        >>> from hanziconv import HanziConv
        >>> print(HanziConv.same('繁简转换器', '繁簡轉換器'))
        True
        >>> print(HanziConv.same('祢是我的荣耀', '祢是我的榮耀', custom_mapping={'祢': '祢'}))
        True
        """
        t1 = cls.toSimplified(text1, custom_mapping=custom_mapping)
        t2 = cls.toSimplified(text2, custom_mapping=custom_mapping)
        return t1 == t2


del traditional_charmap, simplified_charmap
