all: docs

docs: FORCE
	mkdir -p ~/pages/pyg/docs; \
	cd ~/pages/pyg/docs/; \
	git rm -r *; \
	mkdir -p ~/pages/pyg/docs; \
	cd ~/code/pyg/docs/; \
	make html; \
	cp -r .build/html/* ~/pages/pyg/docs/; \
	cd ~/pages/pyg/docs; \
	git add *; \
	git commit -am "$(MSG)"; \
	git push origin gh-pages; \
	cd ~/code/pyg

FORCE:
