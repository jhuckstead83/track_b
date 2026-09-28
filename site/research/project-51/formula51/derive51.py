#!/usr/bin/env python3
"""Derive the alphabet under the fixed Hangul/NFD/uniform-symbol model.

No ordinate values enter. Exact prime-log coefficient vectors identify weight
classes; rational products order them without a floating-point tie test.
Floating-point contributions are used only for the displayed decimal ledger.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import argparse
import csv
import json
import math
import unicodedata

@lru_cache(None)
def factors(n):
    result = Counter()
    p = 2
    while p*p <= n:
        while n % p == 0:
            result[p] += 1
            n //= p
        p += 1
    if n > 1:
        result[n] += 1
    return result

def signature(coefficients):
    return tuple(sorted((p, e) for p, e in coefficients.items() if e))

def log_argument(sig):
    return Fraction(math.prod(p**e for p, e in sig if e > 0),
                    math.prod(p**(-e) for p, e in sig if e < 0))

def component_name(c):
    cp = ord(c)
    if 0x1100 <= cp <= 0x1112:
        return 'L' + str(cp - 0x1100)
    if 0x1161 <= cp <= 0x1175:
        return 'V' + str(cp - 0x1161)
    return 'T' + str(cp - 0x11A7)

def derive(radix=1438):
    if not 1 <= radix <= 11172:
        raise ValueError('Radix must fit the precomposed Hangul syllable block.')
    symbols = [unicodedata.normalize('NFD', chr(0xAC00 + d))
               for d in range(radix)]
    nL = Counter(s[0] for s in symbols)
    nLV = Counter(s[:2] for s in symbols)
    coefficients = defaultdict(Counter)
    occurrences = Counter()
    for s in symbols:
        parent_sizes = [radix, nL[s[0]], nLV[s[:2]], 1]
        events = list(s) + (['END'] if len(s) == 2 else [])
        for i, event in enumerate(events):
            occurrences[event] += 1
            coefficients[event].update(factors(parent_sizes[i]))
            coefficients[event].subtract(factors(parent_sizes[i + 1]))
    total = Counter()
    for coeff in coefficients.values():
        total.update(coeff)
    expected = {p: radix*e for p, e in factors(radix).items()}
    assert dict(signature(total)) == expected, 'Exact chain-rule ledger failed'
    end_signature = signature(coefficients.pop('END'))
    groups = defaultdict(list)
    for c, coeff in coefficients.items():
        groups[signature(coeff)].append(c)
    # All contributions have the same denominator radix. log is increasing.
    ordered = sorted(groups, key=log_argument, reverse=True)
    contribution = lambda sig: math.fsum(e*math.log2(p) for p, e in sig)/radix
    rows = []
    for sig in ordered:
        for c in sorted(groups[sig], key=ord):
            rows.append({'component': c, 'name': component_name(c),
                         'code_point': f'U+{ord(c):04X}',
                         'occurrences': occurrences[c],
                         'prime_log_coefficients': dict(sig),
                         'weight': contribution(sig)})
    return {'radix': radix, 'components': len(rows),
            'class_sizes': [len(groups[sig]) for sig in ordered],
            'lowest': [component_name(c) for c in sorted(groups[ordered[-1]])],
            'visible_sum': math.fsum(row['weight'] for row in rows),
            'end': contribution(end_signature),
            'exact_ledger': 'sum of coefficient vectors = radix * factors(radix)',
            'rows': rows}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', nargs='?', type=Path)
    parser.add_argument('--radix', type=int, default=1438)
    args = parser.parse_args()
    result = derive(args.radix)
    if args.csv:
        with args.csv.open(newline='', encoding='utf-8') as handle:
            archived = list(csv.DictReader(handle))
        assert [r['component'] for r in result['rows']] == [r['component'] for r in archived]
        diff = max(abs(a['weight'] - float(b['importance_bits_per_complete_symbol']))
                   for a, b in zip(result['rows'], archived))
        assert diff < 1e-13, 'Archived weights do not agree at displayed precision'
        assert all(a['occurrences'] == int(b['inventory_occurrences'])
                   for a, b in zip(result['rows'], archived))
        result['archived_max_absolute_difference'] = diff
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))

if __name__ == '__main__':
    main()
