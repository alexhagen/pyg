all: docs

docs: FORCE
	MSG="$(shell git log -1 --pretty=%B | tr -d '\n')"
	@echo $(MSG)
	pandoc README.md -o docs/README.rst; \
	mkdir -p ~/pages/pyg/docs; \
	cd ~/pages/pyg/docs/; \
	git rm -r *; \
	mkdir -p ~/pages/pyg/docs; \
	cd ~/code/pyg/docs/; \
	make html; \
	cp -r .build/html/* ~/pages/pyg/docs/; \
	cd ~/pages/pyg/docs; \
	git add *; \
	git commit -am "$(shell git log -1 --pretty=%B | tr -d '\n')"; \
	git push origin gh-pages; \
	cd ~/code/pyg

FORCE:
