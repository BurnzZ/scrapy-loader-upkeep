init:
	pip3 install pipenv --upgrade
	pipenv install --three --skip-lock
	pipenv install --three --skip-lock --dev

test:
	tox

ci:
	pipenv run pytest --cov --cov-config .coveragerc --verbose

coverage:
	codecov

build:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf *.egg-info .eggs dist .pytest_cache .tox dist/ build/
