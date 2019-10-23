.PHONY: clean

clean:
	rm -rf *.egg-info
	rm -rf build dist

init:
	pipenv --three
	pipenv install
	pipenv install --dev

uninstall:
	pip uninstall spar

local-install:
	pip install --no-cache-dir dist/spar*.tar.gz

build:
	python setup.py sdist bdist_wheel

test-publish:
	twine upload -r pypitest dist/spar*

test-install:
	pip install --no-cache-dir --index-url https://test.pypi.org/simple/ spar

publish:
	twine upload -r pypi dist/spar*
