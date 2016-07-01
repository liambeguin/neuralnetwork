
learn:
	./run.py

plot: prep
	gnuplot -c ./scripts/plot comp $N

prep:
	./lib/preprocessing.py

clean:
	rm -rf out/ plot/


plot_simple: prep
	gnuplot -c ./scripts/plot simple $N

plot_train:
	gnuplot -c ./scripts/plot train $N

