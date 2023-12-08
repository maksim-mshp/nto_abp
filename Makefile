.PHONY: build
build:
	flet pack 'app/main.py' \
	--icon "app/favicon.png" \
	--product-name "NTO_ABP" \
	--product-version "1.4" \
	--file-version "1.0" \
	--file-description "NTO_ABP" \
	--copyright "2023" \