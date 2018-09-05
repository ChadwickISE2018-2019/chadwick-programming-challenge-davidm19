#!/usr/bin/env python
#
# Extracts archive and runs setup script.
#

from __future__ import print_function
import base64
import tarfile
import shutil
import tempfile
import os
import sys
import argparse


def main():
    ap = argparse.ArgumentParser(description='Self-extracting install script')
    ap.add_argument('--check', action='store_true', help='Check hash and exit')
    ap.add_argument('--extract', action='store_true',
                    help='Extract package contents and exit')
    args = ap.parse_args()

    tmp_dir = None
    orig_dir = None
    try:
        # Create a temporary working directory
        tmp_dir = tempfile.mkdtemp()

        # Write the tarfile into the temporary directory
        tar_path = os.path.join(tmp_dir, tar_name)
        with open(tar_path, 'wb') as fp:
            fp.write(base64.decodestring(PKG_DATA))

        if md5_sum:
            import hashlib
            BLOCKSIZE = 65536
            md5 = hashlib.md5()
            with open(tar_path, 'rb') as tar_file:
                buf = tar_file.read(BLOCKSIZE)
                while buf:
                    md5.update(buf)
                    buf = tar_file.read(BLOCKSIZE)
            if md5_sum != md5.hexdigest():
                raise RuntimeError('MD5 checksum mismatch.  The file may be '
                                   'corrupted or incomplete.')
            print('===> MD5 is good')
        else:
            print('===> MD5 not checked')

        if args.check:
            return 0

        if label:
            print(label)

        # Unpack the tarfile.
        with tarfile.open(tar_path) as t:
            t.extractall(tmp_dir)
        os.unlink(tar_path)

        pkg_path = os.path.join(tmp_dir, pkg_name)
        if args.extract:
            print('Extracted package:', pkg_path)
            tmp_dir = None
            return 0

        if script_name:
            sys.path.insert(0, pkg_path)
            orig_dir = os.getcwd()
            os.chdir(pkg_path)
            arch_path = os.path.join(pkg_path, 'install_files')
            sys.path.insert(0, arch_path)
            if in_content:
                os.chdir(arch_path)

            sys.argv = [script_name]
            sys.argv.extend(script_args)
            with open(script_name) as f:
                code = compile(f.read(), script_name, 'exec')

            if not in_content:
                # Setup script expects to be run from in content dir, even if
                # it was not located in archive dir.
                os.chdir(arch_path)

            exec(code, {'__name__': '__main__'})
            # *** DO NO EXPECT EXECUTION PAST THIS POINT ***
            # setup script may call sys.exit()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1
    finally:
        if orig_dir:
            os.chdir(orig_dir)
        # Clean up our temporary working directory
        if tmp_dir:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    return 0

tar_name = 'setup.tar.gz'
md5_sum = 'd1bdd0601b7f8085555e188de75a9eac'
label = None
pkg_name = 'setup'
script_name = 'install.py'
in_content = True
script_args = ('JD', 'jddevaug@gmail.com')

PKG_DATA = b"""
H4sICM2ieVsC/3NldHVwLnRhcgDtPV1v20iSymAPhyWwuHk53MNigRplMZIwEiVKlrTwQpg4GU/G
u/laR5ndIBvILbJlcUyyOWxStubj4fYH7x+4l6vq5pcUO3Yyjj0zYMW2xGZ1d3VVV3U12VWRPE7C
bu2DQg9hPByqT4TtT/XdGgwGo0HfGliIZ/Wt4U4NhrUbgETGLAKoRULEb8O77P724H4hIJX83QC5
4Hmzhetx2f0g8h+/i/yHvd6okv9tyd9nJ7wTRuIbbsemXF6L/EejnQvlP+qPSf49qzcYDWmeWOPx
YFCDXiX/Dw53P+nO3aA7Z3JpGO4CXkHnO/jjk73H+/D6zxAveWAAAreXAhr7ZyFOCe4AD1ZuJAKf
BzGsWOSyucfTWrGAOQeHL9yAO2ZD1z5zY7CMhVvqYv/x3sGjd+9DV7ukE9VS/UHEWewGx5BOZViI
KCXy1I2XwH3memmLdcNATYDOmRH50IkW+mZH6YPhnzhutFESrklHJPcWYIJSITNcQ6pF9FV3o9s2
/FWBU27FDuFrdhyxIKbrjVu3qv/FOK7P/r9F//tDq6f1f9Abjgc90n/8qfT/JsD1QxHFIJM5aonN
pTTSEpF/i/i3CZdxfi3XxddlErueYSwi4WMNM2SoV+k9fhaywEkkjwzDQFXN1KPZ2jWUwoaRG8TN
+kuRAIs4sLlIYtJsEkhMZgG+FjGPHrG5JBVGRfF9Umd7ia3w4Jib9Va5ob0FYsMam1uiJdgP8KoN
DGLXx+JT1/PIZqjG0bogaQpVlS/ZisMOLEUSya1Gp4J442ODiI3NiOhkC+NgoRsSieeA555wGoPN
Apt7bcRBlsKD6eGjzx5QOQ4yirca6EyKf/BMVVDEE/59fuwGUELopHXdIEziZou+am4So2FCwjFZ
dLx6Zb3WVlEZuVJ5X5cTbiZYk5pqLOM4lLvdrrNi/e+CIJJ9k59xO4l5h4WumcgOZzLuWCbz2Xci
YKfStIXfjbGFruJqJxfM50TMpAGfaao+g8anig5VpL61NNG4GkQmVo4TObOFw+GTCfR7vV11s2BR
4yXxPm8ebMXrQMQliZrwzEMC6WYQM7T23wjJwyXS6Hkscu6taC55OJeI6kYr7+HbxEU+5peaacFq
RiZ/AvXuSlvouib4Lk5yMv14VzZTNF35nBs42HoXGbDiUf0qSF2HiW6Kqf58efBof/Z478nBl/vP
p0jNq2YjxZzNkIvBbIY2utGG80pb7XxMG5A3QZ3NZm7gxtvNbN+5uKnD/b0vHu+bvkO1i4uLKzgs
ZqYzJ/Tsa+tc3NcFF9QcgGb9gQjXpP9qkUrZREt6U0Z2G50BGbdQLTaZVswkbapQ+OGaGtCVyjKo
419qBEqTgdyV2SxgPp/NYILTIeNwfTfVwtSkGbVfKJy3/ueCvMb932jn4vW/3x/i+t8fDvDrTh/x
rFF/ZFXr/03AU1T4lctPcU1+mS2HuIB7XPndDKS6gEPUpUXiwd6zA7TppIVfekyeQJNWDVw0FnRl
hsIWwhTRcdcRtuz2TKvfbRm01D7/26M9z15yf62r0EJzenpqym89pstVtZZpGA95rLz259quI2F7
gNsT1y7oQrdeBLhqS7T/PIDTyI1j/MT1csm9EI65Wq2LlYFGhisyREkAuJIrbwX9C0MiukdK7OLS
IxbK50BPY4WXDqSGH+biDOZrCNjKPdb7CewnWxaUH4HNBlR+FK7jpQgG5gg6PmhjeoQjOrKdvMKR
cS6WYaRuhAhxIMh2jstYQYMitK0HtVSL35wcJk/5GrQCK9I51ggFGkuZyogKcbXzkUjDw60SYgsP
juwk8oiuaYR7lniXCMQSaHjCZt5SyHj3TwhdG1VDoO/0uetMrAaSOEUZy/JECTjyCSnwheMu1nD0
5jJ0ZMJBACHKwbUTXIf1GMjdy4WZEmqg1GZZl+i3OU75CkeWhLhi8LwQFklg0zyQWr4bBJW4s8S6
HjfQuoFE30uSnJXzJNUukHxOdLkST9GBywdOE35m81BNsTnX1EXiNDBhunSDE3WVHC81x51jbtjo
dUhwkohwlZe4OVFNzbFUcCLw1hnDqInzmKaWOBP+jjtjarCB7MKdrouzwGnj1NCua0SixX5whhul
yqouDfxt/k/adrx0pcY/RV2yab9MPRALlNtIpdhdbPgsOslHl/rn6FYrzkfaQZaSGKaloB0zZhMb
yddWjnnmXxvGfZqwKAYvsU/aOK02PP0pZ36tgttc/83U7HSvcf2//Pk/rf+9cW8wpvV/2K+e/9++
/H1mo8n7yW8E3ln+/d7AGlTy//nI3+ELhktk96bkb43xo5L/z07+KzeKE+ahS9y9fvmPRyOrv0Pv
f/o71rDS/1uTf/pk5lrf/168/++X9L/Y/1vV/v9GADfmbszpOZrPYhjUPq7duVO7h/yo1T5KfzO4
g7+/2bq+DD6qmR//3+8I+b9e1PCnggoqqKCCCiqooIIKKqigggp+PfC/zTv/+T9/+MOdf92N6TVk
9soy+/zoweH+3nQfpnv3H+1D/kKzafzWdeDgyXT/4f4hPHk6hScvHj1qg/HbhRvJWB1Dga/3Dh98
tXfYHPRbdMdjF9zQL/CyQqvXU6XPDg8e7x2+hL/uv4Sm67SMlt6b/7uGPxVUUEEFFVRQQQUVVFBB
BRVUUMGvAj6+8x+1//597b7reX8Ry0CK4LzzHw+fXl/sB8El8Z/WcJDHf4ytHYr/HI4Go+r8x03A
V3wN39sscFw6Xf9j2zD+zhsrTgHLkITAzo+8VHFXdJI/Cz/QB8NPcF5JE6YiP5oObtzO4yyN7Hh+
Ot2y6OfNkJD08FkSqvDCljr7/7U+d3ZfnG3h5ufR8vCRp4HNdRAoBXWmPVG3Sy45xKcCHB7ywOGB
7XKpiaPYEEecBp5gThYE8uagDTXSUlg6hRwy7E0d4y9Fch8pmo+ymG99nF9mwQV+GK/BcSNuxyJa
ZwEkxlEW65GERyrUQOrD9Bt0pePdIMIwkN901l7Ki3BU4EvegZRLiv4oRxdEnDlrHThB8aYqbiQb
diE/3UwRvpLFtHTzkZYIN4ow3iJgF/bUxBKLlCVZVG4aegBp35IeaJZYpAdW4rBpqOggissh0lXw
TR61hlQ8ETHfzWN/kaIs7Pc0HbQaigp/SONjzCKqpRwNrGJ5s7m8ORbDeCiEc34QQ8yZ/4nxSwgK
PM/+lxh9ffb/4vi/3sAaa/s/Hvb6O32K/7fGw8r+3wSkskZbGyzc4yTizXq/3kKrAz/ooh8MAP3N
XPkmBcNNoJ4HE3VLlrKI/65v1Ekj6iKslpvruuphNf9BhdGu5qZ+C+J+x+EV1HV41Mqvt2HXddpQ
73QS1F8s5haW1R1XYvOByhNSV6HCaNAN+q1cvGvQ/zQi7Vr9vyud/+/v4N8Rnf8lk1Cd/75d+VMa
gJuVf37+e9wb9iv5/wzkX0oD8eHW//FoK/6/b1njKv/XjYCKhS+i8LPkPQ+El/hBGw6CmB9TBPbz
mMKbjS10k5/FpsNtj0Usdlc8q14qms2Z5MYF3Wi/f4Y+gxu8gUTJATJECvY2jPuU32XyRuvNlmFg
CSXayc9SEGoLdJaO2Uwdw8jSeEAjO3LRSLPQOFioR9zMBxxGrs+i9eyEryfTKMFtEEti4QZIMm2p
VFmaKqR0PCNvR/OLTmNonOKgxoUoWaqezdt0dAPHp1mEdzdY1mwgj1zc63S73SKfCo3d9HnMVFFa
gdKU6EobyUou1f9wbTMUx2zWvTn737f6o8r+37b9LyUV+KD7vxHu+zb9v36PpkFl/28AMvtK+Vu0
AVZfM7ursry0s0xhqYVW08NE85CvFnmijgssuYj8DFdylSmC0mBFhvFcX1GCslJ5c+4GziSzViwM
8b6ipJklY0KL2Gg0sDrOXvVcJs9WApFIYm7CQZwmoJBteLg/bcOzp8+nOpPIsxfTIqkdNXMPuzBV
vWYjb6jRBrShS+HIyas6tkAbT2pDfb6Y1l+3VFa7DJ3S2pEVT+sgxd+DqrYL5cwmW8musjZ3NxKe
nIP0gnC2UqBsof2Yp1TTYzM1KfRQLSWqyIYVIeOivPzVZo3XzTQ9W4qlk/t8I0WAu/Jm/SBYMQ/X
zENdqd5qw06vpwXykKeP/FIS6ckdi7GftFyG3HYXLncoJwxKMkYUemjI0yQs5fQ24LlIkrF/xuj5
myL+LnZKJMmNTnQ6TypBqiwT8f4IV8hoY2w0SM+jc6ovb+JttQt6Sp5Bg166NK5AW1FnoqtcpaPC
vWikL3au0lVea5JXeq9RKa16PxK2RvvpOSTRvCJNK6tRpm0ytx+pJUlT+WV4M+XbZdObRcfSxGaa
DddpbCIWFshE3GjdzGxay8RFEadpXmBSkxOwWqYI+BvdBQuhVb8YWB12cwSzKD437R2qes6BjXp5
6UXVlPe4UUWVXITuOhu4rnMu4o8Xm4FXG2N+jUagnxmBPQftHytYSy+JcNqQN0rueqbvSiaUJpTb
sVJoY8mZw6NdqD8Q6IYHcWe6Duk5fhh6rq1yKXWp+7qab/QNxFxl9lU5H12VhAutDeWBjMFg5Ym6
OUPRAnmOaZRsy11Q6YI5ER7w02IncchtETlA1RygOQlfCG6oSd356nJK/6n52vmHWn+g40Dj+/Lc
wMFSo/UNwWMhdlL/sZFVf4sVuguZPc442vTxrn6L8QYLWMGE1k8cxPuS+y58LmyO3hx9g+WO4PfW
bCkEvR+8GUHk6oXXb5BwtXFnRqy8zGdGLMQKJStFdo5obpazxBJOq6yN9enTL57uwkGWaqyeKqDq
6YVyFDaUMNL8zRlarMSkvxT9T7YPjAt0E95FN42LdDOgFTpNtFc2D9qxMVUWvHQdRx5LlUmMn6Eb
QIl8d3o7wKNIqBd6mgvc2dThbNzURiRO9WjJKdCZ4Fb6HZ7Shp+kyi+yCYRmdBesNlyzSl9tHIVO
3ENuvbc6vDmYjcmetX0l2rNpvuWpfpCZvpWbtZHtVxu6L+XTJ0GTyJw0eqb6h0497UImRHarelt0
yf7/Gp79vN/zn96wev9ze/Iv/UcE1/IC6N3//5+xev5fyf925E/m2dWPuaUZn8Uf+vxHr29t6z89
Bqye/93E+x/14K94VFetiRVUUEEFFVRQQQUVVPDrhf8HRILvtAB4AAA=
"""

if __name__ == "__main__":
    sys.exit(main())
