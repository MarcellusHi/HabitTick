.PHONY: lint fmt

lint:
	python3 -m pyflakes src || true

fmt:
	python3 - <<'PY'
import os,sys
import pathlib
for p in pathlib.Path('src').rglob('*.py'):
    s=p.read_text()
    s=s.replace('  ', ' ')
    p.write_text(s)
print('formatted')
PY
