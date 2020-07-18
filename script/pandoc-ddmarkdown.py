#!/usr/bin/env python
# author: RShirohara

import re
from pandocfilters import toJSONFilters, RawInline


PATT_RUBY = re.compile(r"{(.*?)\|(.*?)}")
PATT_TCY = re.compile(r"\^(.*?)\^")


def ruby(key, value, format, meta):
    if key == "Str" and re.search(PATT_RUBY, value):
        result = re.sub(PATT_RUBY, r"<ruby>\1<rt>\2</rt></ruby>", value)
        return RawInline("html", result)


def tate_chu_yoko(key, value, format, meta):
    if key == "Str" and re.search(PATT_TCY, value):
        result = re.sub(PATT_TCY, r"<span class=\"tcy\">\1</span>", value)
        return RawInline("html", result)


if __name__ == "__main__":
    toJSONFilters((ruby, tate_chu_yoko))
