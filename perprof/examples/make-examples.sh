#!/bin/bash

set -e

command -v perprof > /dev/null 2>&1 || { \
  echo >&2 "perprof not installed or I could not find it"; exit 1; }

lang=en
case $1 in
  -l | --lang )
    case $2 in
      en | pt_BR )
        lang=$2
        ;;
      *)
        echo "Unrecognized language $2. Choose from {en, pt_BR}."
        exit 1
        ;;
    esac
    ;;
  *)
    ;;
esac

rm -rf plots
mkdir -p plots

args="-l $lang --pgfplotcompat 1.5"

for p in --performance-profile --performance-profile-multiple-files
do
  suffix=$(echo $p | sed 's/--\(.*\)-.*/\1/g')
  for backend in --tikz --mp
  do
    perprof $p $backend $args --demo -o plots/abc-$suffix
    perprof $p $backend $args --demo --semilog -o plots/abc-semilog-$suffix
    perprof $p $backend $args --demo --semilog --black-and-white -o plots/abc-semilog-bw-$suffix
    perprof $p $backend $args --demo --background 255,255,255 --semilog -o plots/abc-whiteplot-$suffix
    perprof $p $backend $args --demo --page-background 0,0,0 --semilog -o plots/abc-blackpage-$suffix
    perprof $p $backend $args --demo --page-background 0,0,0 --background 255,255,255 --semilog -o plots/abc-blackpage-whiteplot-$suffix

    if [ $suffix == "performance" ]; then
      # Specific for performance profile (or not implemented for others yet)
      perprof $p $backend $args --demo --semilog --subset hs.subset -o plots/abc-semilog-hs-$suffix
      perprof $p $backend $args --demo --tau 100 --semilog -o plots/abc-100-$suffix
      perprof $p $backend $args --demo --maxtime 100 --semilog -o plots/abc-t100-$suffix
      perprof $p $backend $args --demo --mintime 1 --semilog -o plots/abc-m1-$suffix
      if [ $p == "--performance-profile-multiple-files" ]; then
        perprof $p $backend $args --demo --semilog --compare optimalvalues --infeasibility-tolerance 1e-8 -o plots/abc-optimalvalues-$suffix
      fi
    fi
  done
done
