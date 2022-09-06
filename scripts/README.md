# What is this folder?

This is the scripts, currently used to initialize the database with data downloaded from covidtracking.com api.

Read the notebook for more information and some db performance testings
## How to convert notebook to python

```[python]
jupyter nbconvert --to python <notebook-name>.ipynb
```
[ref1](https://stackoverflow.com/questions/35545402/how-to-run-an-ipynb-jupyter-notebook-from-terminal)
[ref2](https://github.com/jupyter/nbconvert)


## Running the script (.py)

```[shell]
    $ cd <project-root>
    $ python manage.py runscript load_csv_to_database
```
