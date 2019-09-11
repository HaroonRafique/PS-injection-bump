#!/bin/bash

# Check if directories needed exist, if not, create them

if [ ! -d "MADX_Tables" ]; then
  mkdir MADX_Tables
fi
if [ ! -d "MADX_Twiss" ]; then
  mkdir MADX_Twiss
fi
if [ ! -d "PTC_Twiss" ]; then
  mkdir PTC_Twiss
fi
if [ ! -d "PTC-PyORBIT_Tables" ]; then
  mkdir PTC-PyORBIT_Tables
fi
if [ ! -d "PyORBIT" ]; then
  mkdir PyORBIT
fi

mv PTC-PyORBIT_flat_file.flt PyORBIT/
mv BSEXT40.tfs MADX_Tables
mv BSEXT42.tfs MADX_Tables
mv BSEXT43.tfs MADX_Tables
mv BSEXT44.tfs MADX_Tables
mv BDIP40.tfs MADX_Tables
mv BDIP42.tfs MADX_Tables
mv BDIP43.tfs MADX_Tables
mv BDIP44.tfs MADX_Tables
mv PI.BSM40.1.tfs MADX_Tables
mv BSEXT_Out.tfs MADX_Tables
mv *.tfs MADX_Twiss
mv MADX_Twiss/madx_twiss.tfs .
mv *.ptc PTC_Twiss
./clean_folder.sh
