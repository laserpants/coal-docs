#!/bin/bash

mkdir -p tmp

pdflatex -output-directory=tmp fold.tex
pdflatex -output-directory=tmp unfold.tex
pdflatex -output-directory=tmp fold_unfold.tex
pdflatex -output-directory=tmp product_coproduct.tex
pdflatex -output-directory=tmp reduce.tex
pdflatex -output-directory=tmp reduce_left.tex

magick -density 600 tmp/fold.pdf -resize 22% -bordercolor white -border 0x0 png/fold.png
magick -density 600 tmp/unfold.pdf -resize 20% -bordercolor white -border 0x0 png/unfold.png
magick -density 600 tmp/fold_unfold.pdf -resize 20% -bordercolor white -border 0x0 png/fold_unfold.png
magick -density 600 tmp/product_coproduct.pdf -resize 20% -bordercolor white -border 0x0 png/product_coproduct.png
magick -density 600 tmp/reduce.pdf -resize 20% -bordercolor white -border 14x14 png/reduce.png
magick -density 600 tmp/reduce_left.pdf -resize 20% -bordercolor white -border 14x14 png/reduce_left.png
