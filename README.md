# python-flowty-examples

[![Gitter](https://badges.gitter.im/flowty/community.svg)](https://gitter.im/flowty/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Install with

```bash
pip intall cffi
pip install --index-url https://test.pypi.org/simple/ --no-deps flowty
```

To run examples to

```bash
pip install python-igraph networkx scipy matplotlib
```

If your are on the development version of `python-flowty` then update the shared libraries.

Optionally make a virtual environment first

```bash
python -m venv .venv
source .venv/bin/activate
```

for Windows do

```dos
python -m venv .venv
.venv\Scripts\activate
```

Download and install `python-flowty`

```bash
cd ../python-flowty
python download_libflowty.py
pip install -e .
cd ../python-flowty-examples
```
