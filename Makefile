all: docs publish

docs: FORCE
	cd ~/code/pyg/; \
	jupyter nbconvert docs/readme_pyg.ipynb --to html --template=basic --execute; \
	mv docs/readme_pyg.html docs/readme.html; \
	jupyter nbconvert docs/readme_pyg.ipynb --to markdown --execute; \
	# sed 's/_static/docs\/_static/g' docs/pym_readme.md > README.md;\
	mv docs/readme_pyg.md README.md; \
  cd ~/code/pyg/docs; \
	make html; \

publish: FORCE
	mkdir -p ~/pages/pyg; \
	cd ~/pages/pyg; \
	git rm -r *; \
	cd ~/code/pyg/docs; \
	cp -r _build/html/* ~/pages/pyg; \
	cd ~/pages/pyg; \
	git add *; \
	touch .nojekyll; \
	git add .nojekyll; \
	git commit -am "$(shell git log -1 --pretty=%B | tr -d '\n')"; \
	git push origin gh-pages; \
	cd ~/code/pyg

FORCE:
