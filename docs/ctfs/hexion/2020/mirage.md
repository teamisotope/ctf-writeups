# Mirage

## Description

"Your eyes can deceive you; don't trust them."
-- Obi-Wan Kenobi

[https://mirage.hexionteam.com](https://mirage.hexionteam.com)

![Mirage](/ctfs/hexion/2020/assets/images/mirage.png)

## Solution

The flag is encoded in a font (hexFont) that has some glyphs rearranged. Doing some simple deduction and replacement, you get: `hexCTF{Don7_judge_a_B0Ok_by_1ts_c0v3r}`

## Script

[mirage.py](/ctfs/hexion/2020/assets/scripts/mirage.py)
```py
strng = "j4teqybvAskIE2S}4IdIc_M5IB8IHmlIF_0Ypn"

alphabet = {
   "d": "a",
   "B": "b",
   "F": "c",
   "S": "d",
   "4": "e",
   "f": "f",
   "}": "g",
   "j": "h",
   "Z": "i",
   "E": "j",
   "5": "k",
   "g": "l",
   "R": "m",
   "s": "n",
   "A": "o",
   "K": "p",
   "O": "q",
   "p": "r",
   "l": "s",
   "m": "t",
   "2": "u",
   "0": "v",
   "x": "w",
   "t": "x",
   "8": "y",
   "h": "z",
   "w": "A",
   "c": "B",
   "e": "C",
   "v": "D",
   "o": "E",
   "y": "F",
   "G": "G",
   "z": "H",
   "1": "I",
   "T": "J",
   "J": "K",
   "{": "L",
   "V": "M",
   "D": "N",
   "M": "O",
   "Q": "P",
   "3": "Q",
   "9": "R",
   "i": "S",
   "q": "T",
   "u": "U",
   "C": "V",
   "7": "W",
   "W": "X",
   "X": "Y",
   "N": "Z",
   "_": "0",
   "H": "1",
   "L": "2",
   "Y": "3",
   "U": "4",
   "a": "5",
   "P": "6",
   "k": "7",
   "r": "8",
   "6": "9",
   "b": "{",
   "n": "}",
   "I": "_"
}

newStr = ""

for c in strng:
    newStr = newStr + alphabet[c]

print(newStr)
```
