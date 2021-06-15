#!/usr/bin/env bash
set -euo pipefail

analysis="ThreeTop"
selection="NEWtopTagger-HT250-Bjet1-Leptons2"

for year in 2016 2017 2018; do
    run_file="run_files_$year.dat"
    analysis_dir="${analysis}_${year}_${selection}"

    if [ ! -f $run_file ]; then
        ./get_files_hdfs.sh $analysis_dir > $run_file
    fi

    if [[ -d "/nfs_scratch/$USER/$analysis_dir-analyze" ]]; then
        rm -r "/nfs_scratch/$USER/$analysis_dir-analyze"
    fi

    farmoutAnalysisJobs "$analysis_dir" \
        --input-file-list=$run_file \
        --infer-cmssw-path --fwklite analyze.py \
        --input-basenames-not-unique \
        --output-dir="/store/user/$USER/${analysis}_${year}_blah" \
        --extra-usercode-files="src/analysis_suite/data/scale_factors"
done
