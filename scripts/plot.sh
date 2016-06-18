#!/bin/bash

type="${1:-comp}"
prefix="${type}_"
col="26"
out_dir="plot/${type}"
dir_raw="raw"
dir_tst="out"
mkdir -p $out_dir


gp_file_list(){
	local dir="$1"
	local num="$2"
	local col="$3"

	out="plot $(find ${dir} -name ${num}\*.txt -exec echo "\"{}\" using ${col}, " \;)"
	echo $out | sed 's/,$//g'
}

plot_simple() {
	for i in $(seq 1 9) ; do
		files="plot $(find ${dir} -name $i\*.txt -exec echo "\"{}\" using ${col} title \"${i}\", " \;)"
		files="$(echo $files | sed 's/,$//g')"
		cat << EOF | gnuplot
set terminal png size 1920,1080
set output '${out_dir}/${i}.png'
set title "$prefix$i"
set style data linespoints
$files
EOF
	done
}

plot_comp(){
	for i in $(seq 1 9) ; do
	cat << EOF | gnuplot
set terminal png size 1920,1080
set output '${out_dir}/${i}.png'
set multiplot layout 4,1
set style data linespoints
set nokey

set title "raw-stat_$i"
$(gp_file_list $dir_raw $i 13)
set title "comp-stat_$i"
$(gp_file_list $dir_tst $i 13)
set title "raw-dyn_$i"
$(gp_file_list $dir_raw $i 26)
set title "comp-dyn_$i"
$(gp_file_list $dir_tst $i 26)
EOF
	done
}



case "$type" in
	raw) dir="raw" plot_simple;;
	test)dir="out" plot_simple;;
	comp) plot_comp ;;
	*) echo "bad arg"; exit 1;;
esac

