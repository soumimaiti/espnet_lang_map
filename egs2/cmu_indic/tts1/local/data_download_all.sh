#!/usr/bin/env bash

# Copyright 2021 Peter Wu
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)
#set -evx
db_root=$1
spk=all


# check arguments
if [ $# != 1 ]; then
    echo "Usage: $0 <db_root>"
    exit 1
fi

set -euo pipefail

cwd=$(pwd)
#download all spk
#skip - guj_dp guj_ad guj_kt   kan_plv 
for spk in hin_ab tel_ss tel_kpn tel_sk tam_sdr mar_slp mar_aup ben_rm pan_amp
do
    if [ ! -e "${db_root}/${spk}.done" ]; then
        mkdir -p "${db_root}"
        cd "${db_root}" || exit 1;
        wget http://festvox.org/h2r_indic/cmu_indic_${spk}.tar.bz2
        tar xf cmu_indic_${spk}.tar.bz2
        rm cmu_indic_${spk}.tar.bz2
        cd "${cwd}" || exit 1;
        echo "Speaker" $spk ":Successfully finished download."
        touch ${db_root}/${spk}.done
    else
        echo "Already exists. Skip download."
    fi
done


# combine the data
mkdir -p ${db_root}/cmu_indic_all/wav
mkdir -p ${db_root}/cmu_indic_all/etc
#skip - guj_dp guj_ad guj_kt   kan_plv 
if [ ! -e "${db_root}/cmu_indic_all/txt.done.data" ]; then
    cd . > ${db_root}/cmu_indic_all/etc/txt.done.data
    for spk in hin_ab tel_ss tel_kpn tel_sk tam_sdr mar_slp mar_aup ben_rm pan_amp
    do
        echo "Combine Speaker: "$spk
        if [ $(ls ${db_root}/cmu_indic_all/wav/${spk}* | wc -l) -lt 300 ]; then
            find ${db_root}/cmu_indic_${spk}/wav -name "*.wav" -follow | sort | while read -r filename;do
                cp ${filename} ${db_root}/cmu_indic_all/wav/${spk}_$(basename $filename)
            done
        fi
        
        sed  's/( /( '"${spk}"_'/' ${db_root}/cmu_indic_${spk}/etc/txt.done.data >> ${db_root}/cmu_indic_all/etc/txt.done.data
    done
fi

perl -pi -e 's/\r//g' ${db_root}/cmu_indic_all/etc/txt.done.data

#TODO check number of files ? 
file_num_wav=$(ls ${db_root}/cmu_indic_all/wav | wc -l)

if [ $file_num_wav -lt 7924 ] ; then
    echo "Error: Wrong file number: " $file_num ". Some files are missing."
    exit 1
fi

echo "Successfully finished download and combine all speakers."
