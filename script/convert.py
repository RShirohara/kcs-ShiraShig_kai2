#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: RShirohara


import re
import sys
from argparse import ArgumentParser

import MeCab


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str)
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("-n", "--no_output", action="store_true")
    parser.add_argument("-p", "--part", type=str)
    return parser.parse_args()


def get_data(path):
    if path:
        with open(path, "r") as _file:
            data = _file.read()
    else:
        data = sys.stdin.read()
    return data


def main(source, part):
    # 全角スペース除去 U+3000
    data = "\n".join([re.sub("^　", "", x) for x in source.splitlines()])
    # 表記揺れ検出
    cab = MeCab.Tagger(
        "-d /usr/lib/mecab/dic/mecab-ipadic-neologd --unk-feature 未知語")
    wakati = [
        re.split(r"[,\t]", i) for i in cab.parse(data).splitlines()][:-1]
    word = dict()
    for i in wakati:
        key = word.keys()
        if i[1] in ("記号", "未知語") or (part and i[1] not in part):
            continue
        yomi = "".join(
            [re.split(r"[,\t]", x)[8] for x in cab.parse(i[7]).splitlines()
             if x != "EOS"])
        if yomi not in key:
            word[yomi] = [i[7]]
        elif i[7] not in word[yomi]:
            word[yomi].append(i[7])
    for yomi, kaki in word.items():
        if len(kaki) > 1:
            print(f"{yomi}: {','.join(kaki)}")
    return data


if __name__ == "__main__":
    args = get_args()
    source = get_data(args.input)
    data = main(source, args.part)
    if args.output:
        with open(args.output, "w") as _file:
            _file.write(data)
    elif not args.no_output:
        print(data)
