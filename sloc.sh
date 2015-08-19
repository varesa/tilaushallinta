#!/bin/sh

py=$(wc -l $(find -name "*.py" | grep -v libs)   | grep total | sed "s|\([0-9]*\) total|\1|")
pt=$(wc -l $(find -name "*.pt" | grep -v libs)   | grep total | sed "s|\([0-9]*\) total|\1|")
css=$(wc -l $(find -name "*.css" | grep -v libs) | grep total | sed "s|\([0-9]*\) total|\1|")
js=$(wc -l $(find -name "*.js" | grep -v libs)   | grep total | sed "s|\([0-9]*\) total|\1|")

echo Lines: python $py, templates $pt, css $css, javascript $js
echo Total: $(echo $py + $pt + $css + $js | bc)
