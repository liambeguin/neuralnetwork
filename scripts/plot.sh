#!/bin/bash

type="${1:-comp}"
prefix="${type}_"
column="${2:-26}"
count="$3"

dir_raw="train"
dir_tst="out"

out_dir="plot/${type}"
mkdir -p $out_dir


gp_file_list(){
	local dir="$1"
	local num="$2"
	local col="$3"

	out="plot $(find ${dir} -name ${num}\*.txt -exec echo "\"{}\" using ${col} smooth csplines, " \;)"

	if [ -z "$count" ]; then
		echo $out | sed 's/,$//g'
	else
		echo $out | cut -d',' -f1-$count
	fi

}

plot_simple() {
	for i in $(seq 1 9) ; do
		cat << EOF | gnuplot
set terminal png size 1920,1080
set output '${out_dir}/${i}.png'
set style data lines
set nokey

set title "$prefix$i"
$(gp_file_list $dir $i $column)
EOF
	done
}

plot_comp(){
	for i in $(seq 1 9) ; do
	cat << EOF | gnuplot
set terminal png size 1920,1080
set output '${out_dir}/${i}.png'
set multiplot layout 4,1
set style data lines
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

plot_all(){
	local dir="$1"
	for i in $(seq 1 9) ; do
	cat << EOF | gnuplot
set terminal png size 1080,3840
set output '${out_dir}/${i}.png'
set multiplot layout 14,1
set style data lines
set nokey

set title "C1_$i"
$(gp_file_list $dir $i 1)
set title "C2_$i"
$(gp_file_list $dir $i 2)
set title "C3_$i"
$(gp_file_list $dir $i 3)
set title "C4_$i"
$(gp_file_list $dir $i 4)
set title "C5_$i"
$(gp_file_list $dir $i 5)
set title "C6_$i"
$(gp_file_list $dir $i 6)
set title "C7_$i"
$(gp_file_list $dir $i 7)
set title "C8_$i"
$(gp_file_list $dir $i 8)
set title "C9_$i"
$(gp_file_list $dir $i 9)
set title "C10_$i"
$(gp_file_list $dir $i 10)
set title "C11_$i"
$(gp_file_list $dir $i 11)
set title "C12_$i"
$(gp_file_list $dir $i 12)
set title "SE_$i"
$(gp_file_list $dir $i 13)
set title "DE_$i"
$(gp_file_list $dir $i 26)
EOF
	done
}


case "$type" in
	raw) dir="train" plot_simple;;
	test)dir="out" plot_simple;;
	comp) plot_comp ;;
	all) plot_all $dir_tst;;
	dump) gp_file_list $dir_raw 1 $column ;;
	*) echo "bad arg"; exit 1;;
esac

