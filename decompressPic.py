#!/usr/bin/env python3

"""
Copyright (c) 2017 Graeme Smith

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
--------------------------------------------------------------------------------
"""

import argparse
import binascii
import mmap
import re
from pathlib import Path
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Decompress Hikvision PIC Files')
optional = parser._action_groups.pop() # Edited this line
required = parser.add_argument_group('required arguments')

required.add_argument('-i', '--input', metavar="Filenames", nargs='+', required=True)
required.add_argument('-d', '--directory', metavar="Output Directory", required=True)
optional.add_argument('-p', '--prefix', metavar="Prefix", help="Filename Prefix (Default: Picture)", required=False, default="Picture")
optional.add_argument('-e', '--every', metavar="Number", help="Output every nth picture (Default: 1)", required=False, type=int, default=1)
parser._action_groups.append(optional) # added this line

args = parser.parse_args()

print ("\nHikvision PIC File Decompressor")
print ("-------------------------------")

count = 1
picture = 0

output_dir = Path(args.directory)
output_dir.mkdir(parents=True, exist_ok=True)

print("\nWriting files to: " + str(output_dir.absolute()))

filename = args.prefix + "-" + str(count) + ".jpg"

file_output = output_dir.joinpath(Path(filename).name)

if file_output.exists():
  filelist = output_dir.glob(args.prefix + "-*" + ".jpg")
  for filename in filelist:
    number = int(str(filename.name)[len(args.prefix)+1:-4])
    if number > count:
      count = number
  count += 1
  print("\nExisting Files Found - Starting at number:" + str(count))

for file_input in args.input:

  if Path(file_input).is_file():
    print ("\nDecompressing: %s" % file_input)
  else:
    print ("\nError: %s not found" % file_input)

  start = 0
  end = 0

  with open(file_input, 'rb') as f:
    f.seek(0, 2)
    num_bytes = f.tell()

    print ("File Size: %.2f MB" % float(num_bytes / 1024 / 1024))
    print()
    i = 0
    status = "No files written"
    t = tqdm(total=num_bytes, unit='B', unit_scale=True, unit_divisor=1024, desc="Progress")

    mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

    while 1:

      f.seek(end)

      t.set_description(status)

      start = mm.find(b'\xFF\xD8', end)
      if start == -1:
        break

      end = mm.find(b'\xFF\xD9', start)

      if (picture % args.every == 0):

        filename = args.prefix + "-" + str(count) + ".jpg"

        filename_output = output_dir.joinpath(Path(filename).name)
        file_output = open(filename_output, 'wb')
        f.seek(start)
        jpeg_data = f.read(end - start)
        file_output.write(jpeg_data)
        file_output.close()
        status = "File " + filename + " written"
        count += 1
      picture += 1
      t.update(end - start)

  t.update(num_bytes - t.n)
  t.close()
  f.closed