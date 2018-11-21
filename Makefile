all: clean

clean:
	find . -name "*.html" -o -name "*.csv" | xargs rm -f
