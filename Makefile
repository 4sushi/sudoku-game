deploy:
	python -m pip install build twine
	rm -r build && rm -r dist && rm -r sudoku_game.egg-info || true
	python -m build
	python -m twine upload dist/*
	

.PHONY: deploy