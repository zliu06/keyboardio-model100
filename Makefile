.PHONY: compile flash reference

compile:
	$(MAKE) -C MyModel100 compile

flash:
	$(MAKE) -C MyModel100 flash

reference:
	python3 MyModel100/generate_reference.py
