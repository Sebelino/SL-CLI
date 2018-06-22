.PHONY: clean test coverage

coverage:
	@nosetests -vs --with-coverage \
	               --cover-package=slcli \
	               --cover-package=api \
				   --cover-package=keyreader \
				   --cover-package=platsuppslag \
				   --cover-package=reseplanerare3 \
				   --cover-package=reseplanerare3-journeydetail \
				   --cover-package=reseplanerare3-trip

test:
	@nosetests -vs

classes_slcli.png:
	pyreverse -o png -p slcli ./slcli

packages_slcli.png: classes_slcli.png

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	virtualenv --no-site-packages venv
	source venv/bin/activate && \
	pip install -Ur requirements.txt;

# Beware of circular dependency black magic:
#requirements.txt: venv
#	source venv/bin/activate && \
#	pip freeze > requirements.txt;

clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf .ropeproject
	rm -rf build
	rm -rf dist
	rm -rf SL_CLI.egg-info
	rm -rf locations.xml
