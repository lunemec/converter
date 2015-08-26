all:
	@echo "make zip"


zip:
	if [ -x "converter.zip" ]; then rm converter.zip; fi
	cd converter; zip -0 ../converter.zip bin/* *.py