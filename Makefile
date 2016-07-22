all:
	./run.py

prep:
	tar xzf tidigits.tar.gz

clean:
	rm -rf out/ plot/

plot_simple: prep
	gnuplot -c ./scripts/plot simple $N

plot_train:
	gnuplot -c ./scripts/plot train $N

