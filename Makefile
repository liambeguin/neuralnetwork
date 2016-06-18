
plot: prep
	./scripts/plot.sh comp

prep:
	./preprocessing.py

clean:
	rm -rf out/ plot/
