install_dev:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install wheel mkdocs-material twine

docs-serve:
	mkdocs serve

docs-publish:
	mkdocs build
	mkdocs gh-deploy

pypi-relase:
	rm -rf dist build pybotnet.egg-info
	python3 setup.py sdist bdist_wheel
	twine upload  dist/*

clear:
	rm -rf dist build pybotnet.egg-info site
