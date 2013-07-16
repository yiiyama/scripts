#!/bin/bash

HOME=/afs/cern.ch/user/y/yiiyama
archive=$HOME/archive

saveoutput() {
    local destroot=$1
    local dir=$2

    local source=$HOME/output/$dir

    for f in $(ls $source); do
        if [ -d $source/$f ]; then
            saveoutput $destroot $dir/$f
        elif [ -L $source/$f ]; then
            continue
        else
            [ -d $destroot/$dir ] || mkdir -p $destroot/$dir
            mv $source/$f $destroot/$dir/
            ln -s $destroot/$dir/$f $source/$f
        fi
    done
}

dest=$(date -d yesterday +'%y%m%d')

while [ $# -gt 0 ]; do
    case $1 in
        -d)
            dest=$2
            shift
            shift
            ;;
        *)
            break
            ;;
    esac
done

newdir=$archive/$dest
[ -d $newdir ] && (echo "$newdir exists"; exit 1)
mkdir $newdir

cd $HOME
tar czf $newdir/src.tar.gz src

mkdir $newdir/output
saveoutput $newdir/output .

tar czf $newdir/output.snapshot.tar.gz output

$HOME/scripts/plots.sh $dest
