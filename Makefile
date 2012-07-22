PROJ := double-metaphone
LIB := metaphone
GITHUB_REPO := github.com:oubiwann/$(PROJ).git
PKG_NAME := $(PROJ)
TMP_FILE ?= /tmp/MSG
VIRT_DIR ?= .venv
PYTHON_BIN ?= /System/Library/Frameworks/Python.framework/Versions/2.7/bin
PYTHON ?= $(PYTHON_BIN)/python2.7

log-concise:
	git log --oneline

log-verbose:
	git log --format=fuller

log-authors:
	git log --format='%aN %aE' --date=short

log-authors-date:
	git log --format='%ad %aN %aE' --date=short

log-changes:
	git log --format='%ad %n* %B %N%n' --date=short

clean:
	find ./ -name "*~" -exec rm {} \;
	find ./ -name "*.pyc" -exec rm {} \;
	find ./ -name "*.pyo" -exec rm {} \;
	find . -name "*.sw[op]" -exec rm {} \;
	rm -rf _trial_temp/ build/ dist/ MANIFEST \
		CHECK_THIS_BEFORE_UPLOAD.txt *.egg-info

push:
	git push --all git@$(GITHUB_REPO)

push-tags:
	git push --tags git@$(GITHUB_REPO)

push-all: push push-tags
.PHONY: push-all

stat:
	@echo
	@echo "### Git info ###"
	@echo
	git info
	echo
	@echo "### Git working branch status ###"
	@echo
	@git status -s
	@echo
	@echo "### Git branches ###"
	@echo
	@git branch
	@echo 

status: stat
.PHONY: status

todo:
	git grep -n -i -2 XXX
	git grep -n -i -2 TODO
.PHONY: todo

build:
	$(PYTHON) setup.py build
	$(PYTHON) setup.py sdist

check: clean build
	trial $(LIB)
	-pep8 $(LIB)
	-pyflakes $(LIB)

register:
	$(PYTHON) setup.py register

upload: check
	$(PYTHON) setup.py sdist upload --show-response
