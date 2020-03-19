#2013 Samuel Balula, samuel.balula (you know what) tecnico.ulisboa.pt

#run: gnuplot fit.gnuplot
#or copy past into gnuplot interactive

file = 'pt_20200319' #.dat
f(x) = Io*exp(a*x) #can be any function

set fit logfile file.'.log' #Output file
fit f(x) file.".dat" using 1:2:3 via Io, a    #x, y, ey

set xrange [*: *]
set yrange [* : *]
set xlabel "time since 1st case (days)"
set ylabel "Count (-)"

plot \
f(x) lt rgb "black" title 'f(x)=Io*exp(a*x)',\
file.".dat" notitle with yerrorbars lt rgb "black"

set terminal postscript eps color lw 1 "Helvetica" 20
set output file.'.eps'
replot

set terminal png size 1200,1200 enhanced lw 2 font "Helvetica,20"
set output file.'.png'
replot

#set terminal jpg color enhanced "Helvetica" 20
#set output file.'.jpg'
#replot

#set terminal pdf
#set output file.'.pdf'
#replot

set terminal pop

