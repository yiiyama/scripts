#!/bin/bash

www=/afs/cern.ch/user/y/yiiyama/www
archive=$www/archive

makethumbnail() {
    local parent=$1
    local child=$2
    local target=$parent/$child

    if [ -d $target ]; then
        for f in $(ls $target); do
            [ $child = "png" ] && continue
            makethumbnail $target $f
        done
        [ -d $target/png ] || mkdir $target/png
        mv $target/*.png $target/png/ > /dev/null 2>&1
    else
        [ -n "$(echo $target | grep '.pdf')" ] && convert $target $target.png
    fi
}

makelist() {
    local reldir=$1
    local target=$www/$reldir

    for dir in $(ls $target); do
        [ ! -d $target/$dir ] && continue
        makelist $reldir/$dir
    done

    [ ! -d $target/png ] && return

    rm $target/img.html > /dev/null 2>&1

    for img in $(ls $target/png); do
        if [ -n "$(echo $img | grep '.pdf.png')" ]; then
            ref=$(echo $img | sed 's/pdf[.]png/pdf/')
        else
            ref="png/"$img
        fi
        str="<li><a href='/yiiyama/$reldir/"$ref"' target='_blank'><img src='/yiiyama/$reldir/png/$img' />$ref</a></li>"
        echo $str >> $target/img.html
    done
}

makehtml() {
    local target=$1

    echo "<ul>"

    [ -e $target/img.html ] && cat $target/img.html

    for dir in $(ls $target); do
        [ ! -d $target/$dir -o $dir = "png" ] && continue
        id=$(echo $target/$dir | sed 's|/|.|g')
        echo "<li><div onclick='hideshow(\"$id\")' style='width:800px;text-overflow:ellipsis;white-space:nowrap;'>$dir:"
        for name in $(ls $target/$dir); do
            [ $name = "img.html" -o $name = "png" ] && continue
            if [ -d $target/$dir/$name ]; then
                echo "&nbsp;<span style='color:blue;'>$name</span>"
            else
                echo "&nbsp;$name"
            fi
        done
        echo "</div>"
        echo "<div id='$id' style='display:none;'>"
        makehtml $target/$dir
        echo "</div>"
        echo "</li>"
    done

    echo "</ul>"
}

dest=$(date -d yesterday +'%y%m%d')
htmlonly=0

while [ $# -gt 0 ]; do
    case $1 in
        -d)
            dest=$2
            shift
            shift
            ;;
        -h)
            htmlonly=1
            shift
            ;;
        *)
            break
            ;;
    esac
done

if [ $htmlonly -eq 0 -a -n "$(ls $www/plots)" ]; then
    newdir=$archive/$dest
    [ -d $newdir ] && (echo "$newdir exists"; exit 1)
    mkdir $newdir
    mv $www/plots/* $newdir

    makethumbnail $archive $dest
fi

makelist "archive/$dest"

html=$archive/index.html

echo "<html>" > $html
echo "<head>" >> $html
echo "<title>Plots</title>" >> $html
echo "<style>" >> $html
echo "ul li img { vertical-align:middle; width:100px; }" >> $html
echo "</style>" >> $html
echo "<script type='text/javascript'>" >> $html
echo "function hideshow(id){list = document.getElementById(id); list.style.display = list.style.display == 'block' ? 'none' : 'block';}" >> $html
echo "</script>" >> $html
echo "</head>" >> $html
echo "<body>" >> $html
makehtml $archive >> $html
echo "</body>" >> $html
echo "</html>" >> $html
