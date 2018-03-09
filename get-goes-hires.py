#!/usr/bin/env python
"""Download NOAA CLASS full-fidelity data
1. request NOAA CLASS data via shopping cart (free)
2. you will be sent an email with FTP commands in 24-48 hours.
3. Within 96 hours of that email, copy and paste FTP commands to text file.
   Copy from the "cd ..." command through all the "get ..." commands
4. Load and process that text file with this program.
"""
from time import sleep
from pathlib import Path
import ftplib
try:
    import netCDF4
except ImportError:
    netCDF4 = None

def get_hires(host:str, ftpdir:str, flist:list, odir:Path, clobber:bool=False):
    """download hi-res GOES data over FTP"""

    odir = Path(odir).expanduser()
    print('writing',len(flist),'files to',odir)

    with ftplib.FTP(host,'anonymous','guest',timeout=15) as F:
        F.cwd(ftpdir)

        for f in flist:
            parts= f.split('/')
            rpath = parts[-2]
            rfn = parts[-1]
            if F.pwd().split('/')[-1] != rpath:
                F.cwd(rpath)

            ofn = odir / f
            if not clobber: # check NetCDF4 files to see if we can read them or if they are corrupted by aborted download.
                if ofn.is_file() and ofn.suffix=='.nc':
                    try:
                        if netCDF4:
                            with netCDF4.Dataset(ofn,'r') as n:
                                if n.variables:
                                    continue
                    except Exception:
                        pass

            print(ofn)
            ofn.parent.mkdir(parents=True,exist_ok=True)
            with ofn.open('wb') as h:
                F.retrbinary(f'RETR {rfn}', h.write)

            sleep(1) # anti-leech


def parse_email(txtfn:Path):
    """Parse GOES hi-res file list from email"""
    txtfn = Path(txtfn).expanduser()

    flist = []
    with txtfn.open('r') as f:
        for line in f:
            l = line.strip()
            if l.startswith('get'):
                flist.append(l.split(' ')[-1])
                continue
            if l.startswith('cd'):
                ftpdir = l.split(' ')[-1]

    return ftpdir, flist



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('txtfn',help='text file copied from CLASS email')
    p.add_argument('outdir',help='place to write the files')
    p.add_argument('-host',help='FTP host',default='ftp.class.ngdc.noaa.gov')
    p = p.parse_args()

    ftpdir, flist = parse_email(p.txtfn)

    get_hires(p.host, ftpdir, flist, p.outdir)