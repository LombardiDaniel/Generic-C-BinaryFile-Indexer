APPNAME = c_indexer
TGTDIR = /usr/local/bin

MAIN = main.py
OTHERS = c_indexer


install: $(OTHERS)
	pip install -r requirements.txt
	chmod +x src/$(MAIN)
	cp src/$(MAIN) $(TGTDIR)/$(APPNAME)

c_indexer.py:
	cp src/main.py $(TGTDIR)

# cdi_tracker_utils.py:
# 	cp src/cdi_tracker_utils.py $(TGTDIR)


uninstall:
	rm $(TGTDIR)/$(APPNAME)
	rm $(TGTDIR)/c_indexer.py
	# rm $(TGTDIR)/cdi_tracker_utils.py
	echo "C/C++ Generic Binary file Indexer has been uninstalled."
