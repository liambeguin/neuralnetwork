

plot: prep
	./scripts/plot.sh comp 26 $N

prep:
	./preprocessing.py

clean:
	rm -rf out/ plot/


ts: prep
	./scripts/plot.sh test 13 $N

td: prep
	./scripts/plot.sh test 26 $N

rs: prep
	./scripts/plot.sh raw 13 $N
rd: prep
	./scripts/plot.sh raw 26 $N


single: prep
	echo "plot '$(FILE)' using $(COL) with lines, \
		'out/$(FILE)' using $(COL) with lines" | gnuplot -p
