# trequire

Manage backend resources for terraform states (`.tfstate`). `trequire` means terraform requirements.

## Requirements

* `Python >= 3.6`
*  `aws credentials` file

## Install

For easy deployment this is built as executable. You can download it from [release](https://github.com/wmariuss/trequire/releases) section.

Development

* `pip install pipenv`
* `pipenv install --dev`
* `pipenv run trequire --help` or `pipenv shell` and execute `trequire --help`

Build executable

* `pipenv run tox -e package`

## Usage

* Create a config same as example file from [examples](examples) dir or follow example config bellow
* Run `trequire run -f your_config_file.yaml`

Example config - parameters

```yaml
requirements: # Required
  profile : development # Profile from your AWS credentials file. This is required, if this is not specified default profile is used
  add: # This is optional
    buckets: # Required if add key is specified
      - terraform-dev
      - terraform-staging
      - terraform-prod
    dynamodb: # Required if add key is specified
      - terraform-states
      - terraform-dev
    user: terraform-user # Optional, only if you want a user dedicated for Terraform
  remove: # This is optional. If this not specified nothing is happening
    buckets: # Required if remove key is specified
      - terraform-dev
      - terraform-staging
    dynamodb: # Required if remove key is specified
      - terraform-dev
      - terraform-staging
    user: terraform-user
```

## Tests

Very soon.

## Authors

* [Marius Stanca](mailto:me@marius.xyz)
