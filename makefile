.PHONY: clean test coverage

coverage:
	@nosetests -vs --with-coverage \
	               --cover-package=slcli \
	               --cover-package=api \
				   --cover-package=keyreader \
				   --cover-package=platsuppslag \
				   --cover-package=reseplanerare2 \
				   --cover-package=reseplanerare2-journeydetail \
				   --cover-package=reseplanerare2-trip

test:
	@nosetests -vs

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
	rm -rf SLCLI.egg-info
	rm -rf locations.xml
