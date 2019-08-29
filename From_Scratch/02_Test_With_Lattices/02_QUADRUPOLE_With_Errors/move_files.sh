#!/bin/bash
mv BSEXT40.tfs MADX_Tables
mv BSEXT42.tfs MADX_Tables
mv BSEXT43.tfs MADX_Tables
mv BSEXT44.tfs MADX_Tables
mv BSEXT_Out.tfs MADX_Tables
mv *.tfs MADX_Twiss
mv MADX_Twiss/madx_twiss.tfs .
mv *.ptc PTC_Twiss
./clean_folder.sh
