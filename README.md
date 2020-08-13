# python-flowty-examples

[![Gitter](https://badges.gitter.im/flowty/community.svg)](https://gitter.im/flowty/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Install with

```bash
pip intall cffi
pip install --index-url https://test.pypi.org/simple/ --no-deps --pre --upgrade flowty
```

To run examples do

```bash
pip install networkx scipy matplotlib
```

## Virtual Environment

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

## Jupyter Notebooks

In the notebook repo there are some interactive examples.

Install jupyter

```sh
pip install jupyter
```

If you use a virtual environment add the kernel to jupyter

```sh
python -m ipykernel install --user --name=.venv
```

Remove the kernel again by doing

```sh
jupyter kernelspec uninstall .venv
```
