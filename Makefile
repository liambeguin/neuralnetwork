.PHONY: all gui prep clean
all:
	./run.py

gui:
	./neuralNetworkGui.py

prep:
	tar xzf tidigits.tar.gz

clean:
	rm -rf out/ plot/ test/ train/ validation/
	find . -iname \*.pyc -exec rm {} \;
	rm autoload.save.gz

plot_simple: prep
	gnuplot -c ./scripts/plot simple $N

plot_train:
	gnuplot -c ./scripts/plot train $N

