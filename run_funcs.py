import os
import sys
import subprocess

from parse_funcs import parse


ROOT_DIR = os.getenv('GITHUB_WORKSPACE')

SUPPORTED_LANGS = [
        'ruby',
        'python',
        'perl',
        'node',
        'golang',
        'elixir',
        'haskell',
        'php']

RUN_CMDS = {
        'ruby': 'ruby',
        'python': 'python',
        'node': 'node',
        'perl': 'perl',
        'golang': 'go run',
        'elixir': 'elixir',
        'haskell': 'runhaskell',
        'php': 'php'}


def run_fun(path, func):
    func_lang = func['language']
    if func_lang not in SUPPORTED_LANGS:
        return ""
    func_file_name = func['file_name']
    if func_file_name.strip() == '':
        return ""

    deps_install = {
        'ruby': '[ -e Gemfile ] && bundle install >/dev/null 2>&1',
        'python': '[ -e requirements.txt ] && pip install -r requirements.txt >/dev/null 2>&1',
        'node': '[ -e package.json ] && npm install --only=prod >/dev/null 2>&1',
        'perl': '[ -e cpanfile ] && cpanm --installdeps . >/dev/null 2>&1'}

    cmd = ['docker', 'run', '--rm', '--workdir', '/github/workspace',
           '-v', os.getenv('GITHUB_WORKSPACE') + ':/github/workspace',
           func_lang + ':latest', 'sh', '-c',
           "cd " + path + ";" + deps_install.get(func_lang, ':') + ";" + RUN_CMDS[func_lang] + " " + func_file_name]

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
    path = ROOT_DIR
    if len(sys.argv) > 1:
        path = sys.argv[1]

    funcs = parse(path)

    for func in funcs:
        routes = func['routes']
        if not routes:
            continue
        if len(routes) == 1:
            if routes[0]['action'] != 'GET':
                continue
            result = run_fun(path, func)
            print(result)
            if result.strip() == '':
                continue
            write_to_route(result, routes[0]['route'])
        else:
            results = run_fun(path, func)
            if results.strip() == '':
                continue
            print(results)
            output_list = str.splitlines(results)
            for i in range(len(routes)):
                if 'route' in routes[i] and routes[i]['action'] == 'GET':
                    write_to_route(output_list[i], routes[i]['route'])
