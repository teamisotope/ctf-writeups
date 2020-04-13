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
