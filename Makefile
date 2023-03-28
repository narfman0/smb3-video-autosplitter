default: test

clean: clean-build clean-pyc clean-installer
c: clean

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -f .coverage
	rm -f *.log

clean-installer:
	rm -fr output/
	rm -fr app.spec
	rm -f smb3_video_autosplitter.spec
	rm -f smb3_video_autosplitter.zip

clean-pyc: ## remove Python file artifacts
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*~' -exec rm -f {} +

init:
	pip install -r .

init-dev:
	pip install -r requirements_test.txt

pyinstaller: clean
	pyinstaller --noconfirm --onefile --console \
		-n smb3_video_autosplitter --uac-admin \
		app.py
	cp -r data/ dist/
	cp config.ini.sample dist/config.ini
	cp README.* dist/
	7z a smb3_video_autosplitter.zip dist/*
	7z rn smb3_video_autosplitter.zip dist smb3_video_autosplitter

run-main:
	python -m smb3_video_autosplitter.main

run-test:
	pytest --cov=smb3_video_autosplitter --cov-report term-missing tests/

release-test: clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypitest dist/*

release-prod: clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*

release: run-test release-test release-prod clean

m: run-main
main: init m
t: run-test
test: init-dev t
