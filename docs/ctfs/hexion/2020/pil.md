# PIL

## Description

Our team detected a suspicious image, and managed to get a code of some sort, and we think they are related.

Can you investigate this subject and see if you can give us more data?

## Hint

PIL = PI + IL

## Solution

Some ILCode is provided as well as a bitmap.

![result.bmp](/ctfs/hexion/2020/assets/provided/result.bmp)

`source` ([provided](/ctfs/hexion/2020/assets/provided/source)):
```
.class private auto ansi '<Module>'
{
} // end of class <Module>

.class private auto ansi beforefieldinit csharp.Program
    extends [mscorlib]System.Object
{
    // Fields
    .field private static class [mscorlib]System.IO.FileStream piFile

    // Methods
    .method private hidebysig static 
        void Main (
            string[] args
        ) cil managed 
    {
        // Method begins at RVA 0x2050
        // Code size 38 (0x26)
        .maxstack 8

        IL_0000: ldstr "one-million-digits.txt"
        IL_0005: ldc.i4.3
        IL_0006: ldc.i4.1
        IL_0007: newobj instance void [mscorlib]System.IO.FileStream::.ctor(string, valuetype [mscorlib]System.IO.FileMode, valuetype [mscorlib]System.IO.FileAccess)
        IL_000c: stsfld class [mscorlib]System.IO.FileStream csharp.Program::piFile
        IL_0011: ldstr "original.bmp"
        IL_0016: ldstr "result.bmp"
        IL_001b: ldstr "<CENSORED>"
        IL_0020: call void csharp.Program::Hide(string, string, string)
        IL_0025: ret
    } // end of method Program::Main

    .method private hidebysig static 
        void Hide (
            string srcPath,
            string dstPath,
            string secret
        ) cil managed 
    {
        // Method begins at RVA 0x2078
        // Code size 106 (0x6a)
        .maxstack 5
        .locals init (
            [0] class [mscorlib]System.Collections.BitArray,
            [1] uint8[],
            [2] int32,
            [3] int32,
            [4] uint8,
            [5] int32
        )

        IL_0000: call class [mscorlib]System.Text.Encoding [mscorlib]System.Text.Encoding::get_UTF8()
        IL_0005: ldarg.2
        IL_0006: callvirt instance uint8[] [mscorlib]System.Text.Encoding::GetBytes(string)
        IL_000b: newobj instance void [mscorlib]System.Collections.BitArray::.ctor(uint8[])
        IL_0010: stloc.0
        IL_0011: ldarg.0
        IL_0012: call uint8[] [mscorlib]System.IO.File::ReadAllBytes(string)
        IL_0017: stloc.1
        IL_0018: ldloc.1
        IL_0019: ldc.i4.s 14
        IL_001b: ldelem.u1
        IL_001c: ldc.i4.s 14
        IL_001e: add
        IL_001f: stloc.2
        IL_0020: ldc.i4.0
        IL_0021: stloc.s 5
        // sequence point: hidden
        IL_0023: br.s IL_0058
        // loop start (head: IL_0058)
            IL_0025: ldloc.2
            IL_0026: call int32 csharp.Program::GetNextPiDigit()
            IL_002b: add
            IL_002c: stloc.3
            IL_002d: ldc.i4 254
            IL_0032: ldloc.1
            IL_0033: ldloc.3
            IL_0034: ldelem.u1
            IL_0035: and
            IL_0036: conv.u1
            IL_0037: stloc.s 4
            IL_0039: ldloc.1
            IL_003a: ldloc.3
            IL_003b: ldloc.s 4
            IL_003d: ldloc.0
            IL_003e: ldloc.s 5
            IL_0040: callvirt instance bool [mscorlib]System.Collections.BitArray::get_Item(int32)
            IL_0045: call uint8 [mscorlib]System.Convert::ToByte(bool)
            IL_004a: add
            IL_004b: conv.u1
            IL_004c: stelem.i1
            IL_004d: ldloc.2
            IL_004e: ldc.i4.s 10
            IL_0050: add
            IL_0051: stloc.2
            IL_0052: ldloc.s 5
            IL_0054: ldc.i4.1
            IL_0055: add
            IL_0056: stloc.s 5

            IL_0058: ldloc.s 5
            IL_005a: ldloc.0
            IL_005b: callvirt instance int32 [mscorlib]System.Collections.BitArray::get_Length()
            IL_0060: blt.s IL_0025
        // end loop

        IL_0062: ldarg.1
        IL_0063: ldloc.1
        IL_0064: call void [mscorlib]System.IO.File::WriteAllBytes(string, uint8[])
        IL_0069: ret
    } // end of method Program::Hide

    .method private hidebysig static
        int32 GetNextPiDigit () cil managed 
    {
        // Method begins at RVA 0x20f0
        // Code size 32 (0x20)
        .maxstack 2
        .locals init (
            [0] int32
        )

        IL_0000: ldsfld class [mscorlib]System.IO.FileStream csharp.Program::piFile
        IL_0005: callvirt instance int32 [mscorlib]System.IO.Stream::ReadByte()
        IL_000a: stloc.0
        IL_000b: ldloc.0
        IL_000c: ldc.i4.s 10
        IL_000e: bne.un.s IL_001b

        IL_0010: ldsfld class [mscorlib]System.IO.FileStream csharp.Program::piFile
        IL_0015: callvirt instance int32 [mscorlib]System.IO.Stream::ReadByte()
        IL_001a: stloc.0

        IL_001b: ldloc.0
        IL_001c: ldc.i4.s 48
        IL_001e: sub
        IL_001f: ret
    } // end of method Program::GetNextPiDigit

    .method public hidebysig specialname rtspecialname 
        instance void .ctor () cil managed 
    {
        // Method begins at RVA 0x211c
        // Code size 7 (0x7)
        .maxstack 8

        IL_0000: ldarg.0
        IL_0001: call instance void [mscorlib]System.Object::.ctor()
        IL_0006: ret
    } // end of method Program::.ctor

} // end of class csharp.Program
```

Now, you see, I'm terrible at ILCode, so I compiled it to a DLL:

`ilasm /output:test.dll /dll /debug source`

Then I used ILSpy (the cross-platform command-line version since I'm using Linux):

`ilspycmd test.dll > source.cs`

The source I got:

[PIL.cs](/ctfs/hexion/2020/assets/scripts/PIL.cs)
```csharp
using System;
using System.Collections;
using System.IO;
using System.Text;

namespace csharp
{
	internal class Program
	{
		private static FileStream piFile;

		private static void Main(string[] args)
		{
			piFile = new FileStream("one-million-digits.txt", FileMode.Open, FileAccess.Read);
			Hide("original.bmp", "result.bmp", "<CENSORED>");
		}

		private static void Hide(string srcPath, string dstPath, string secret)
		{
			BitArray bitArray = new BitArray(Encoding.UTF8.GetBytes(secret));
			byte[] array = File.ReadAllBytes(srcPath);
			int num = array[14] + 14;
			for (int i = 0; i < bitArray.Length; i++)
			{
				int num2 = num + GetNextPiDigit();
				byte b = (byte)(0xFE & array[num2]);
				array[num2] = (byte)(b + Convert.ToByte(bitArray[i]));
				num += 10;
			}
			File.WriteAllBytes(dstPath, array);
		}

		private static int GetNextPiDigit()
		{
			int num = piFile.ReadByte();
			if (num == 10)
			{
				num = piFile.ReadByte();
			}
			return num - 48;
		}
	}
}
```

The million digits of Pi start **after** the decimal point (e.g. `14159265...`). This was found out by asking the admins. Thanks admins, you're doing great!

The algorithm works like this (pseudocode):
```
Initial conditions:
* bitmap = OpenTheFile("original.bmp").ExtractItsBytesIntoAnArray(); // we aren't provided the original, but it's required to encode
* flag = ExtractBitsFrom("<INSERT FLAG HERE>");
* num = bitmap[14] + 14;
Algorithm:
* for every bitIndex in the flag,
  * num2 = num + GetNextPiDigit();
  * b = ClearLastBit(bitmap[num2]);
  * bitmap[num2] = b + GetBitAsZeroOrOne(flag[i]);
  * num = num + 10;
End of loop:
* OpenTheFile("result.bmp").WriteBytes(bitmap);
```
To decode this, you simply have to go use the same loop but replace these two instructions:

```
b = ClearLastBit(bitmap[num2]);
bitmap[num2] = b + GetBitAsZeroOrOne(flag[i]);
```

with some type of logic to set a bit in a character to 0 or 1.

Here's the script that I used for this:

(I had to use Python 2 cause it was complaining about non-UTF8 characters in `result.bmp`)

[PIL.py](/ctfs/hexion/2020/assets/scripts/PIL.py)
```python

with open("result.bmp", "r") as file:
    bmp = file.read()

with open("pi.txt", "r") as file:
    pi = file.read()

def getPi():
    global cpi
    cpi += 1
    return int(pi[cpi-1])

cpi = 0

num = ord(bmp[14]) + 14

flagLst = ("a "*64).split(" ")

charNum = 0

for i in range(0, 64): # Going to 64 characters cause I don't know the length of the flag
    for i2 in range(0, 8):
        pin = getPi()
        num2 = num + pin
        charNum |= (0x01 & ord(bmp[num2])) << i2
        # print("num : %d / pi : %d / num2 : %d / charNum : %s" % (num, pin, num2, bin(charNum))) # debugging
        num += 10
    # print(chr(charNum)) # debugging
    flagLst[i] = chr(charNum)
    charNum = 0

flag = "".join(flagLst)
print(flag)
```

Running this script got me:

```
hexCTF{l00k_wh0_l3arned_t0_sp34k_byt3c0de}F��c��u�Ѡ�Y��P,8/
```

That extra gibberish at the end is non-encoded characters, so you can just ignore that.

Extracting that first part of that text gets you the flag.

### Non-Provided References

`pi.txt` is simply a truncated (remove the first two characters, `3.`) version of [pi1000000.txt](https://www.angio.net/pi/digits/pi1000000.txt) from [angio.net](https://www.angio.net/pi/digits.html).
