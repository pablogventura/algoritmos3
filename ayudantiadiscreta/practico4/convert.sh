convert -draw 'text 50,50 "NA 1"'  1.png 1.pdf
convert -draw 'text 50,50 "NA 2"'  2.png 2.pdf
convert -draw 'text 50,50 "NA 3"'  3.png 3.pdf
convert -draw 'text 50,50 "NA 4"'  4.png 4.pdf
convert -draw 'text 50,50 "NA 5"'  5.png 5.pdf
convert -draw 'text 50,50 "NA 6"'  6.png 6.pdf
convert -draw 'text 50,50 "NA 7"'  7.png 7.pdf
convert -draw 'text 50,50 "NA 8"'  8.png 8.pdf
convert -draw 'text 50,50 "NA 9"'  9.png 9.pdf
convert -draw 'text 50,50 "NA 10"'  10.png 10.pdf
convert -draw 'text 50,50 "NA 11"'  11.png 11.pdf
convert -draw 'text 50,50 "NA 12"'  12.png 12.pdf
convert -draw 'text 50,50 "NA 13"'  13.png 13.pdf
convert -draw 'text 50,50 "NA 14"'  14.png 14.pdf
convert -draw 'text 50,50 "NA 15"'  15.png 15.pdf
convert -draw 'text 50,50 "NA 16"'  16.png 16.pdf
pdftk *.pdf cat output temp.pdf
pdfjam temp.pdf --nup 2x2 --outfile salida.pdf
