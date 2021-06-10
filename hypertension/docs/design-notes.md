## Python Environment

`vro-main/poetry.toml` is set to cause the poetry virtualenv of the project to be located in `vro-main/.venv` rather than the default poetry location of `~/Library/Caches/pypoetry/virtualenvs`.

As a result, when you open VS Code to `vro-main/` it will automatically see and activate the virtualenv.

This lets you:
- Run tests using vscode test integration
- Run linters and auto-formatters
- Run individual functions right from the editor

(You can do all of this in VS Code by clicking the debug icon - the settings.json and launch.json config files enable this setup.)

If the virtualenv was not located in `vro-main/.venv`, then when you open VS Code to `vro-main/`, VS Code would pop up an error messge:

> No Python interpreter is selected. You need to select a Python interpreter to enable featuresr such as IntelliSense, linting, and debugging.
