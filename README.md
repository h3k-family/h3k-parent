# h3k parent
![by](https://img.shields.io/badge/by-c3n7-blue)
![license](https://img.shields.io/badge/license-BSD%202%20Clause-green)
[![Python package](https://github.com/c3n7/h3k-parent/actions/workflows/main.yml/badge.svg)](https://github.com/c3n7/h3k-parent/actions/workflows/main.yml)
[![dockerhub](https://img.shields.io/badge/images-Docker%20Hub-9cf)](https://hub.docker.com/repository/docker/c3n7/h3k-parent)  
Part of the ***h3k project***: an attempt at creating a federated system for pooling IoT data.

## Setting up a development enviroment
### (n)vim + coc.nvim
_You can use **nvim** or **vim**, as long as you have `coc.nvim` installed._  
Assuming you've set-up and activated a virtual environment, install `dev-requirements.txt`
```shell
pip install -r dev-requirements.txt
```
To deal with pylint's issues like [No name 'BaseModel' in module 'pydantic'](https://github.com/samuelcolvin/pydantic/issues/1961), add a local config file:
  - In **(n)vim**'s command mode:  
  ```shell
  :CocLocalConfig
  ```
  - The above command will create a `.vim/coc-settings.json` file. Add this to it:
  ```json
  {
    "python.linting.pylintArgs": [
      "--extension-pkg-whitelist=pydantic",
      "--disable=C0114, C0115, C0116, E1101, C0103"
    ]
  }
  ```

### VS Code/Codium
Assuming you've set-up and activated a virtual enviroment, install development requirements:
```shell
pip install autopep8 pylint
```
To deal with pylint's issues like [No name 'BaseModel' in module 'pydantic'](https://github.com/samuelcolvin/pydantic/issues/1961), add a workspace configuration file in `.vscode/settings.json` with the following contents:
  ```json
  {
    "python.linting.pylintArgs": [
      "--extension-pkg-whitelist=pydantic",
      "--disable=C0114, C0115, C0116, E1101, C0103"
    ]
  }
  ```
where `venv/` is the folder containing your virtual environment.

## Building image
1. Build 
    ```shell
    $ docker build -t h3k-parent .
    ```
2. Do a test run (optional)
    ```shell
    $ docker run dp 7800:8080 h3k-parent
    ```
3. Stop it once done testing.
    ```shell
    $ docker stop image_name
    ```
4. Tag it, where `username` is your docker hub's username.
    ```shell
    $ docker tag h3k-parent username/h3k-parent
    ```
5. Push it
    ```shell
    $ docker push username/h3k-parent
    ```

---
_**H**aba na **h**aba, **h**ujaza **k**ibaba._
