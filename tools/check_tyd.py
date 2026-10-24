#!/usr/bin/env python3
"""Sanity-check ModernTech TyD files before starting the game.

Catches unbalanced brackets, duplicate feature names, and references to
categories, name generators, software types, designs or features that don't exist.
Usage: python3 tools/check_tyd.py   (run from the mod folder)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILTIN_TYPES = {"Operating System", "Game", "3D Editor", "2D Editor", "Audio Tool", "Antivirus",
                 "Office Software", "Distribution platform"}
BUILTIN_GENS = {"Company", "None"}
BUILTIN_DESIGNS = {"Console", "OldConsole", "CellPhone", "SmartPhone", "TestJoystick"}
errors = []


def strip_strings(t):
    return re.sub(r'"[^"\n]*"', '""', re.sub(r'(?m)(^|\s)(#|//).*$', '', t))


def values(block, key):
    """All values of `key` lines, unquoted (single values or [ a; b ] lists)."""
    out = []
    for m in re.finditer(rf'(?m)^\s*{key}\s+(.+?)\s*$', block):
        v = m.group(1)
        items = v.strip('[] ').split(';') if v.startswith('[') else [v]
        out += [i.strip().strip('"') for i in items if i.strip()]
    return out


files = sorted(p for p in ROOT.rglob('*.tyd') if 'dist' not in p.relative_to(ROOT).parts)
gens = BUILTIN_GENS | {p.stem for p in (ROOT / 'NameGenerators').glob('*.txt')}
designs = BUILTIN_DESIGNS | {d for f in files if 'HardwareDesign' in f.parts for d in values(f.read_text(), 'ID')}
types = set(BUILTIN_TYPES)
deps = []  # (file, software type, tool type), checked once every type is known

for f in files:
    t = f.read_text()
    s = strip_strings(t)
    if t.count('"') % 2:
        errors.append(f"{f.name}: odd number of quotes")
    for o, c in ('{}', '[]'):
        if s.count(o) != s.count(c):
            errors.append(f"{f.name}: {s.count(o)} '{o}' vs {s.count(c)} '{c}'")
    if not t.lstrip().startswith('SoftwareType'):
        continue
    types.add(values(t, 'Name')[0])
    head, _, feats = t.partition('\n\tFeatures')
    cats = set(re.findall(r'(?m)^\t{3}Name\s+"?([^"\n]+?)"?\s*$', head))
    fnames = re.findall(r'(?m)^\t{3,5}Name\s+"?([^"\n]+?)"?\s*$', feats)
    for n in {n for n in fnames if fnames.count(n) > 1}:
        errors.append(f"{f.name}: duplicate feature name '{n}'")
    for c in values(feats, 'SoftwareCategories'):
        if c not in cats:
            errors.append(f"{f.name}: SoftwareCategories '{c}' is not a category")
    for g in values(t, 'NameGenerator'):
        if g not in gens:
            errors.append(f"{f.name}: missing name generator '{g}'")
    for d in values(t, 'DependsOn'):
        if d not in fnames:
            errors.append(f"{f.name}: component DependsOn unknown feature '{d}'")
    for d in values(t, 'Design'):
        if d not in designs:
            errors.append(f"{f.name}: unknown hardware design '{d}'")
    # Rules from the game's GameData.CheckForErrors: one spec per main feature group, the Hardware spec only on
    # Console/Phone apps, no zero dev times, tools must be other software types
    specs = re.findall(r'(?m)^\t{3}Spec\s+"?([^"\n]+?)"?\s*$', feats)
    for sp in {sp for sp in specs if specs.count(sp) > 1}:
        errors.append(f"{f.name}: spec '{sp}' is used by more than one main feature group")
    if 'Hardware' in specs and set(values(head, 'OSSupport')) - {'Console', 'Phone'}:
        errors.append(f"{f.name}: Hardware spec is only supported on Console and Phone operating systems")
    if any(float(v) == 0 for v in values(feats, 'DevTime')):
        errors.append(f"{f.name}: a feature has zero DevTime")
    deps += [(f.name, values(t, 'Name')[0], d) for d in values(feats, 'Dependencies')]

for fname, sw, d in deps:
    if d == sw or d not in types:
        errors.append(f"{fname}: Dependencies '{d}' must be another existing software type")

for f in (ROOT / 'CompanyTypes').glob('*.tyd'):
    t = f.read_text()
    for sw in values(t, 'Software'):
        if sw not in types:
            errors.append(f"{f.name}: unknown software type '{sw}'")
    for g in values(t, 'NameGen'):
        if g not in gens:
            errors.append(f"{f.name}: missing name generator '{g}'")

print('\n'.join(errors) or f"OK: {len(files)} TyD files checked")
sys.exit(1 if errors else 0)
