import re
from subprocess import check_output


def get_new_toc():
    new_toc = check_output(
        'markdown-toc README.md',
        shell=True
    ).decode('utf-8')

    pattern = ['<!-- toc -->', '', new_toc, '', '<!-- tocstop -->']

    return '\n'.join(pattern)


def get_readme():
    with open('README.md', 'r') as f:
        return f.read()


def save_readme(readme):
    with open('README.md', 'w') as f:
        return f.write(readme)


def replace_toc():
    readme = get_readme()
    new_toc = get_new_toc()

    regex = '<!-- toc -->(.|\n)+<!-- tocstop -->'

    new_readme = re.sub(regex, new_toc, readme)

    save_readme(new_readme)

    print('TOC updated ...')


def main():
    return replace_toc()


if __name__ == '__main__':
    main()
