# ActionServerless - Use GitHub Actions to create a serverless service

[![ActionServerless Testing](https://github.com/gitx-io/ActionServerless/workflows/Test%20run%20funcs/badge.svg)](https://github.com/gitx-io/ActionServerless/blob/master/.github/workflows/test_run_funcs.yml)

ActionServerless is an action using [GitFx](https://github.com/gitx-io/GitFx) to do some computing and then generate a string/JSON file to a path, you can visit the file as a service when in dev/testing, or even in your production. We may take it as a GitHub Actions powered `serverless` service.

In fact you can do all of these in native GitHub actions. ActionServerless just wraps the steps to simplify the work:

1. you can focus on coding the real logic, no need to care too much setup steps on the languages that ActionServerless supported(JS/Ruby/Python/Perl etc.). With [a template](https://github.com/gitx-io/ActionServerless-template) we provide, you even don't bother to edit the action workflow configuration.
2. use the route grammer we defined to specify a path to store the generated string/JSON file, that makes the job easy and clear.

## Quick start

At first [use the template](https://github.com/gitx-io/ActionServerless-template/generate) to create a repository. Then We start with a Python example:

```python
# function.py
import json

# GET /api/py_hello.json

print(json.dumps({"hello": "world"}))
```

put the file to a path(default is the root path of a repo, otherwise you need add the path as an argument to your actions configuaration),  when you push the code the action will be triggered. Then the program's output is written to a file located in `api/py_hello.json` that you defined as a route in the comment.

more languages' examples you can find [here](https://github.com/gitx-io/GitFx/tree/master/test/func_examples).

## Languages supported

See: https://github.com/gitx-io/GitFx#languages-supported


## Documents

* [before_script](https://github.com/gitx-io/GitFx/wiki/before_script)
* [HTTP Headers](https://github.com/gitx-io/GitFx/wiki/HTTP-Headers)

## Real world examples

* [Shell functions to get Docker image versions](https://github.com/gitx-io?q=docker-major-versions&type=public&language=shell&sort=name)

## Contributions

Contributions are welcome! You may check the following features in case you'd like to contribute but no idea what to do:

* Support to add your favorite languages
* Support dependency installation to the existing languages
* Use this action to create an application and share it

