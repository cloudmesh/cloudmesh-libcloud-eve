all:
	rm -f specification/all.*
	cd specification; cms schema cat . all.json
	cms schema convert specification/all.json aws.py
	cms admin rest init specification/all.settings.py 

#cms schema convert specification
