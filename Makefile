
.PHONY: sys-env dev-configure dev-env


sys-env:
	# install homebrew, the unofficial package manager for Macs
	# from https://brew.sh/
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	
	# then pyenv, for managing multiple python versions
	# from https://github.com/pyenv/pyenv
	brew install pyenv
	# then pyenv-virtualenv, a plugin to help managing python virtual environments
	brew install pyenv-virtualenv
	# configure shell environment to recognize pyenv and pyenv-virtualenv
	echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
	echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
	
	# install pipsi, variant of pip for keeping global python installs inside virtualenvs
	curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python
	# configure shell environment to recognize pipsi
	echo 'export PATH=/Users/gordo/.local/bin:$PATH' >> .profile
	
	# reset your entire shell env 
	exec "$SHELL"


aws-configure:
	# install aws command line tools
	pipsi install awscli
	# configure aws credentials
	aws configure --profile rji
	# you'll be prompted to provide
	# AWS Access Key ID 
	# AWS Secret Access Key
	# Default region name
	# Default output format 


dev-env:
	# install the latest version of python
	pyenv install 3.6.3
	# set up a virtual environment that uses the latest version of Python
	pyenv virtualenv 3.6.3 django-fact-checker-py36
	# connect the project directory to the virtual environment
	pyenv local django-fact-checker-py36
	# install the projects dependencies
	pip install -r requirements-dev.txt
