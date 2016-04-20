venv: venv/bin/activate

venv/bin/activate: requirements.txt
	virtualenv --no-site-packages venv
	source venv/bin/activate && \
	pip install -Ur requirements.txt;

# Beware of circular dependency black magic:
#requirements.txt: venv
#	source venv/bin/activate && \
#	pip freeze requirements.txt;

clean:
	rm *.pyc
