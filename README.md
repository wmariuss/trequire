# trequire

Manage backend resources for terraform states (`.tfstate`). `trequire` means terraform requirements.

## Requirements

* `Python >= 3.6.x` by `pyenv`
* `aws credentials`

## Install

* `pip install trequire` or using this repo `pip install .`

Development

* `pip install pipenv`
* `pipenv install --dev`
* `pipenv run trequire --help` or `pipenv shell`

## Usage

* Create a config same as `example_config.yaml` file or follow example config bellow
* Run `trequire run -f your_config_file.yaml`

Example config - parameters

```yaml
requirements: # Required
  profile : development # Profile from your AWS credentials file. This is required, if this is not specified default profile is used
  add: # This is optional
    buckets: # Required if add key is specified
      - bucket1
      - bucket2
      - ...
    dynamodb: # Required if add key is specified
      - table1
      - table2
      - ...
  remove: # This is optional. If this not specified nothing is happening
    buckets: # Required if remove key is specified
      - bucket1
      - bucket2
      - ...
    dynamodb: # Required if remove key is specified
      - table2
      - table2
      - ...
```

## Tests

Very soon.

## Authors

* [Marius Stanca](mailto:me@marius.xyz)