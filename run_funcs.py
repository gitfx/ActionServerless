import os
import sys
import subprocess

from parse_funcs import parse


ROOT_DIR = os.getenv('GITHUB_WORKSPACE', os.path.dirname(os.path.abspath(__file__)))

SUPPORTED_LANGS = [
        'ruby',
        'python',
        'perl',
        'node',
        'golang',
        'elixir',
        'haskell',
        'php',
        ]

RUN_CMDS = {
        'ruby': 'ruby',
        'python': 'python',
        'node': 'node',
        'perl': 'perl',
        'golang': 'go run',
        'elixir': 'elixir',
        'haskell': 'runhaskell',
        'php': 'php',
        }

DOCKER_IMAGES = {
        'php': 'composer',
        }


def docker_image(lang):
    """you can specify a docker image name for a language,
    otherwise the language name will be returned as the image name"""
    return DOCKER_IMAGES.get(lang, lang)

def run_fun(func_path, func):
    func_lang = func['language']
    if func_lang not in SUPPORTED_LANGS:
        return ""
    func_file_name = func['file_name']
    if func_file_name.strip() == '':
        return ""

    # pre_hook script is a shell script that start with a same name of
    # the function file but ends with '.sh',
    # will be run before the function running
    pre_hook_file = func_file_name + '.sh'
    run_pre_hook = '[ -f {0} ] && sh {0} >/dev/null 2>&1'.format(pre_hook_file)

    deps_install = {
        'ruby': '[ -f Gemfile ] && bundle install >/dev/null 2>&1',
        'python': '[ -f requirements.txt ] && pip install -r requirements.txt >/dev/null 2>&1',
        'node': '[ -f package.json ] && npm install --only=prod >/dev/null 2>&1',
        'perl': '[ -f cpanfile ] && cpanm --installdeps . >/dev/null 2>&1'}

    cmd = ['docker', 'run', '--rm', '--workdir', '/github/workspace',
           '-v', ROOT_DIR + ':/github/workspace',
           docker_image(func_lang) + ':latest', 'sh', '-c',
           "cd " + os.path.relpath(func_path, ROOT_DIR) + ";" +
           deps_install.get(func_lang, ':') + ";" +
           run_pre_hook + ";" +
           RUN_CMDS[func_lang] + " " + func_file_name]

    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return output.decode("utf8")

def write_to_route(result, func_route):
    if func_route.strip() == '':
        return

    dst_dir = os.path.join(ROOT_DIR, os.path.dirname(func_route))
    if dst_dir and not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    file_path = os.path.join(ROOT_DIR, func_route)
    f = open(file_path, 'w')
    f.write(result)
    f.close()

    print_github_raw_url(func_route)

def print_github_raw_url(file_path):
    repo_name = os.getenv('GITHUB_REPOSITORY')
    branch = os.getenv('GITHUB_REF')
    if not repo_name or not branch:
        return
    branch = branch.split('/')[-1]
    base_url = 'https://raw.githubusercontent.com/{}/{}'.format(repo_name, branch)
    raw_url = os.path.join(base_url, file_path)
    if raw_url:
        print(raw_url)


if __name__ == "__main__":
    # func_path is a path where the functions locate
    func_path = ROOT_DIR
    if len(sys.argv) > 1:
        func_path = sys.argv[1]
    func_path = os.path.abspath(func_path)

    funcs = parse(func_path)

    for func in funcs:
        routes = func['routes']
        if not routes:
            continue
        if len(routes) == 1:
            if routes[0]['action'] != 'GET':
                continue
            result = run_fun(func_path, func)
            print(result)
            if result.strip() == '':
                continue
            write_to_route(result, routes[0]['route'])
        else:
            results = run_fun(func_path, func)
            if results.strip() == '':
                continue
            print(results)
            output_list = str.splitlines(results)
            for i in range(len(routes)):
                if 'route' in routes[i] and routes[i]['action'] == 'GET':
                    write_to_route(output_list[i], routes[i]['route'])
