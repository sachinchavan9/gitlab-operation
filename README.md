# GitLab Delete Issue

Either install the package via pip or run the code directly from this repository:

## either: Install via pip

install from pip
```
pip install gitlab-issue-delete
```

usage
```
$ gitlab-issue-delete
```

## or: Run directly from repository

To install all needed python modules, run
```
python3 -m pip install -r requirements.txt
```

From the base path of this repository, execute:
```
python3 -c "import gitlab_operations.deleteissue; gitlab_operations.deleteissue.main()"
```

## Execution

Follow the instructions on screen.

you need `gitlab` and `accesstoken` 

default config file found at

```
$HOME/.config/gitlab/config
```