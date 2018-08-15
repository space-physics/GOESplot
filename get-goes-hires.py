#!/usr/bin/env python
"""Download NOAA CLASS full-fidelity data
1. request NOAA CLASS data via shopping cart (free)
2. you will be sent an email with FTP commands in 24-48 hours.
3. Within 96 hours of that email, copy and paste FTP commands to text file.
   Copy from the "cd ..." command through all the "get ..." commands
4. Load and process that text file with this program.
"""
import goes_quickplot.io as gqio
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('txtfn', help='text file copied from CLASS email')
    p.add_argument('outdir', help='place to write the files')
    p.add_argument('-host', help='FTP host', default='ftp.class.ngdc.noaa.gov')
    p = p.parse_args()

    ftpdir, flist = gqio.parse_email(p.txtfn)

    gqio.get_hires(p.host, ftpdir, flist, p.outdir)


if __name__ == '__main__':
    main()
