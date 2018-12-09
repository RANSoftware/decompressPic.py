The purpose of this script is to retrieve the JPEG images embedded in a PIC file created by a Hikvision CCTV.

Usage:
Required flags:
    -i or --input filename(s)     : list of PIC files to be decompressed
    -d or --directory directory   : directory to output the files, if the
                                      directory doesn't exist it will be
                                      created
Optional flags:
    -p or --prefix name           : filenames will start with this prefix
                                    and end in '-nnn.jpg' where nnn is the
                                    number of the image in the sequence.
                                    Defaults to 'picture'
    -e or --every n               : only output every nth image. Defaults
                                    to 1
                                    
If the script detects existing image files with the same prefix it will try to continue the sequence.
