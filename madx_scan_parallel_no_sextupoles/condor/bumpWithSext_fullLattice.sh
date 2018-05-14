#!/bin/bash
# Condor submission job file

# get condor variables
OrigIwd=`grep "^OrigIwd" .job.ad | cut -d'"' -f2`
ClusterId=`grep "^ClusterId" .job.ad | tr -dc '0-9'`
ProcId=`grep "^ProcId" .job.ad | tr -dc '0-9'`

# copy all files from initial directory
cp -r ${OrigIwd}* .

# run the madx caller that calculates the params and every time twiss with
# a different set of parameters
python ./madx_caller.py

# move results to the result folder
mv *.out result/out/
mv *.twiss result/twiss/

# copy files back to initial directory
cp -r result/ ${OrigIwd}
