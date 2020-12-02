# -*- coding: utf-8 -*-
"""
Created on Wed May 20 18:56:52 2020

@author: O136114O
"""
import sys
import re
import os
from os import listdir
import os.path, time
from os.path import isfile, join
import shutil

# path = sys.argv[1]
#--------------------------------------------------------------------
print('----------------------------\n')
path = str(input('path: \t'))
os.chdir(path)

print('----------------------------\n')
grp_by = str(input('Group by d "day", m "month", y "year" \t'))
map_grp_by = {'d':'%d-%m-%Y' ,'m':'%m-%Y','y':'%Y' }

print('----------------------------\n')
expt_str = str(input('any exeptions (txt, pdf, png ...)?  if nothing, type none: \t'))
expt_set = set()
if expt_str != 'none':
    expt_set = set(list(expt_str.split(" ")))
print('----------------------------\n')
#--------------------------------------------------------------------



files = [f for f in listdir(".") if (isfile(join(".", f)) and os.path.splitext(f)[1].replace('.','') not in expt_set)]
# files.remove('cluster_by_date.py')


dates = {}

for f in files:
    t = time.strftime(map_grp_by[grp_by], time.gmtime(os.path.getctime(f)))
    if t not in dates :
        dates[t]=[f]
    else :
        dates[t].append(f)
#--------------------------------------------------------------------
def max_id(d, f):
    file_ids = []
    file_extention = os.path.splitext(f)[1].replace('.','')

    files = [f for f in listdir(".//"+d) if (isfile(join(".//"+d, f)) and os.path.splitext(f)[1].replace('.','') == file_extention) ]

    for f in files:
        file_ids.append(int(re.findall("\d+", f)[-1]))

    return max(file_ids)

#--------------------------------------------------------------------

def rename(d,f):

    new_id = max_id(d,f)+1
    old_id = re.findall('[0-9]+', f)[-1]
    new_f = f.replace(old_id, str(new_id))

    # new = os.path.splitext(f)[0]+str(i)+os.path.splitext(f)[1]

    return new_f

#--------------------------------------------------------------------

for d in dates:

    if os.path.exists(d):
        for f in dates[d]:
            if os.path.exists(d+'//'+f):

                new = rename(d,f)
                os.rename(r''+f,r''+new)
                dest = shutil.move(new, d)
            else:

                dest = shutil.move(f, d)

    else :

        try:
            os.mkdir(d)
            for f in dates[d]:
                dest = shutil.move('.//'+f, d)

        except OSError:
            print ("Creation of the directory %s failed" % d)
        else:
            print ("Successfully created the directory %s " % d)
