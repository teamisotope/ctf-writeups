#!/bin/env python3

import argparse
import sys
import requests
import hexdump
from os import path


class PiSteg(object):

    def __init__(self, input_file=None, output_file=None):
        self.piSource = requests.get("https://teamisotope.com/pi.txt")
        self.piIndex = 0
        if not self.piSource.status_code:
            raise ConnectionError("Error: bad status code while getting pi source")
        self.input_file = input_file
        self.output_file = output_file

    def get_pi_digit(self):
        number = self.piSource.text[self.piIndex]
        self.piIndex += 1
        return int(number)

    def encode(self, secret):
        input_array = bytearray(self.input_file.read())

        raw_index = input_array[14] + 14

        for char_index in range(0, len(secret)):
            for bit_index in range(0, 8):
                pi_digit = self.get_pi_digit()
                dest_index = raw_index + pi_digit

                input_array[dest_index] = 0xFE & input_array[dest_index]  # Clear last bit
                bit = (ord(secret[char_index]) & (0x01 << bit_index)) >> bit_index  # Set bit if set at index in secret
                input_array[dest_index] = input_array[dest_index] + bit  # Set last bit to 0 or 1 through addition
                raw_index += 10

        self.output_file.write(input_array)

    def decode(self, length):
        input_array = bytearray(self.input_file.read())

        raw_index = input_array[14] + 14

        secret = bytearray(b"\x00" * length)

        current_byte = 0

        for char_index in range(0, length):
            for bit_index in range(0, 8):
                pi_digit = self.get_pi_digit()
                dest_index = raw_index + pi_digit
                current_byte |= (input_array[dest_index] & 0x01) << bit_index
                raw_index += 10
            secret[char_index] = current_byte
            current_byte = 0

        return secret

    def close(self):
        if self.input_file is not None:
            self.input_file.close()
        if self.output_file is not None:
            self.output_file.close()
        self.piSource.close()


class PiStegCLI(object):

    def __init__(self):
        self.steg = PiSteg()
        parser = argparse.ArgumentParser(description='''
                                                     BMP Steganography LSB algorithm with indexes based on Pi.
                                                     Designed by Idan#6062 and yinon#7204 for HexionCTF 2020.
                                                     Script by The Puzzlemaker.
                                                     ''')

        parser.add_argument('command',
                            type=str,
                            nargs=1,
                            help="The action to perform",
                            choices=["encode", "decode"])

        args = parser.parse_args(sys.argv[1:2])

        if args.command[0] == "encode":
            self.encode()
        elif args.command[0] == "decode":
            self.decode()
        else:
            print("Error: invalid command!")
            exit(-1)

    def encode(self):
        parser = argparse.ArgumentParser(description="Encodes a secret in a bitmap")

        parser.add_argument('infile',
                            type=str,
                            nargs=1,
                            help="The input file",
                            metavar="input_file")

        parser.add_argument('outfile',
                            type=str,
                            nargs=1,
                            help="The output file",
                            metavar="output_file")

        parser.add_argument('-s', '--secret-file',
                            type=str,
                            nargs=1,
                            metavar="secret_file",
                            help="A file to input the secret from")

        parser.add_argument('-o', '--overwrite',
                            action='store_true',
                            help="Allow overwriting the encoded result")

        parser.add_argument('secret',
                            type=str,
                            nargs='?',
                            help="A secret to encode")

        args = parser.parse_args(sys.argv[2:])

        secret = ""

        if args.secret_file is None and args.secret is None:
            print("Error: either 'secret' or 'secretFile' is required!")
            exit(-1)
        elif args.secret_file is not None and args.secret is not None:
            print("Error: you can only use either 'secret' or 'secretFile', not both!")
            exit(-1)

        if not path.exists(args.infile[0]):
            print("Error: input file '%s' does not exist!" % args.infile[0])
            exit(-1)
        elif not path.isfile(args.infile[0]):
            print("Error: input file '%s' is not a file!" % args.infile[0])
            exit(-1)

        if path.exists(args.outfile[0]) and not args.overwrite:
            print("Error: output file '%s' already exists!" % args.outfile[0])
            exit(-1)

        if args.secret_file is not None:
            if not path.exists(args.secret_file[0]):
                print("Error: secret file '%s' does not exist!" % args.secret_file[0])
                exit(-1)
            elif not path.isfile(args.secret_file[0]):
                print("Error: secret file '%s' is not a file!" % args.secret_file[0])
                exit(-1)
            secret_file = open(args.secret_file[0], "r")
            if not secret_file.closed:
                secret = secret_file.read()
            else:
                print("Error while opening secret file '%s'!" % args.secret_file[0])
                exit(-1)
            secret_file.close()
        elif args.secret is not None:
            secret = args.secret

        input_file = open(args.infile[0], "rb")
        if input_file.closed:
            print("Error while opening input file '%s'!" % args.secret_file[0])
            exit(-1)

        output_file = open(args.outfile[0], "wb")
        if output_file.closed:
            print("Error while opening output file '%s'!" % args.secret_file[0])
            exit(-1)

        self.steg = PiSteg(input_file, output_file)
        self.steg.encode(secret)
        self.steg.close()
        print("Successfully encoded secret!")

    def decode(self):
        parser = argparse.ArgumentParser(description="Decodes a secret from a bitmap")

        parser.add_argument('infile',
                            type=str,
                            nargs=1,
                            help="The input file",
                            metavar="input_file")

        parser.add_argument('length',
                            type=int,
                            nargs=1,
                            help="Length to encode",
                            metavar='length')

        parser.add_argument('-x', '--hexdump',
                            action="store_true",
                            help="Show output as a hexdump even if decodable with UTF8")

        args = parser.parse_args(sys.argv[2:])

        dump_output = args.hexdump

        if not path.exists(args.infile[0]):
            print("Error: input file '%s' does not exist!" % args.infile[0])
            exit(-1)
        elif not path.isfile(args.infile[0]):
            print("Error: input file '%s' is not a file!" % args.infile[0])
            exit(-1)

        input_file = open(args.infile[0], "rb")
        if input_file.closed:
            print("Error while opening input file '%s'!" % args.secret_file[0])
            exit(-1)

        if args.length[0] <= 0:
            print("Error: length must be greater than 0!")
            exit(-1)

        self.steg = PiSteg(input_file)
        secret = self.steg.decode(args.length[0])
        self.steg.close()
        print("Successfully decoded secret!")
        secretString = ""
        try:
            secretString = secret.decode('utf-8')
            print("Your secret is as follows:")
            if not dump_output:
                print(secretString)
        except UnicodeError:
            if not dump_output:
                print("Your secret was not entirely decodable by UTF8, so the hexdump is as follows "
                      "(this may mean your length is a bit too high, so you may be able to ignore extra data):")
            dump_output = True

        if dump_output:
            hexdump.hexdump(secret)


if __name__ == '__main__':
    PiStegCLI()

