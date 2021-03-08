# ActionServerless - Use GitHub Actions to create a serverless service

[![ActionServerless Testing](https://github.com/gitx-io/ActionServerless/workflows/Test%20run%20funcs/badge.svg)](https://github.com/gitx-io/ActionServerless/blob/master/.github/workflows/test_run_funcs.yml)

ActionServerless is an action to do some computing and then generate a string/JSON file to a path, you can visit the file as a service when in dev/testing, or in your production. We may take it as a GitHub Actions powered `serverless` service.

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

more languages' examples you can find [here](https://github.com/gitx-io/ActionServerless/tree/master/test/func_samples).

## Languages supported

* **Python** (support `requirements.txt` to install deps)
* **Ruby** (support `Gemfile` to install deps)
* **Node.js** (support `package.json` to install deps)
* **Perl** (support `cpanfile` to install deps )
* **Golang** (no deps supported yet)
* **Haskell** (no deps supported yet)
* **Elixir** (no deps supported yet)

## HTTP(s) Headers

If we'd like to be serious to take visiting such a GitHub raw file as a 'service', it's no problem for most situations as you request a normal HTTP(s) service. But GitHub returns a `text/html` for any raw files it serves, that might lead to some bugs though I can't give an example yet.

So we provide a header rewrite service, which returns an `application/json` header for the `json` format files(those generated file suffixed with `.json`), and a `text/plain` header for the rest(those string or any text-based format files).

### Header rewrite usage

Fox example, here's a raw url of the file:

```
https://raw.githubusercontent.com/gitx-io/ActionServerless/master/README.md
```

its corresponding header-rewritten url should be:

```
https://gitx.io/j/gitx-io/ActionServerless/master/README.md
```

just use `gitx.io/j/` to replace the `raw.githubusercontent.com/` segment.

