import re
import os
import sys
import tomli


with open('../pyproject.toml', 'rb') as f:
    config = tomli.load(f)


def reformat_line(line, codeblock, admonition, depth):
    base_link = config['project']['urls']['Documentation']
    while True:
        match = re.search('{(\\S+)}`(\\S+|.+<\\S+>)`', line)
        if match is None:
            break
        role, target = match.groups()
        if role in ['class', 'meth', 'attr']:
            anchor = target.replace('~', '')
            names = anchor.split('.')
            label = f'``{names[-1]}``'
            link = f'reference/{names[1]}.html#{anchor}'
        elif role == 'doc':
            if target == '/':
                label = 'documentation'
                link = ''
            else:
                label, link = target[:-1].split('<')
                link = f'{link}.html'
        else:
            raise NotImplementedError(f'The role {role} is not implemented.')
        link_element = f'[{label}]({base_link}/{link})'
        line = line[:match.span()[0]] + link_element + line[match.span()[1]:]
    if re.search('```', line):
        codeblock = not codeblock
    if not codeblock:
        if line.startswith('#'):
            line = depth * '#' + line
    if re.search('````', line):
        admonition = not admonition
        if admonition:
            match = re.search('````{(\\S+)}', line)
            line = line.replace(match[0], f'[!{match[1].upper()}]')
        else:
            line = ''
    if admonition:
        line = '> ' + line
    return line, codeblock, admonition


def generate_readme(input_file, output_file):
    readme_content = []

    templatedir = os.path.dirname(input_file)
    pattern = r'<!---\s*(.*?)\s*-->'
    codeblock = False
    admonition = False

    with open(input_file, 'r') as file1:
        for line1 in file1:
            match1 = re.search(pattern, line1)
            if match1:
                with open(f'{templatedir}/../{match1.group(1)}', 'r') as file2:
                    for line2 in file2:
                        match2 = re.search(pattern, line2)
                        if match2:
                            with open(f'{templatedir}/../{match2.group(1)}', 'r') as file3:
                                for line3 in file3:
                                    line3, codeblock, admonition = reformat_line(line3, codeblock, admonition, 2)
                                    readme_content.append(line3)
                        else:
                            line2, codeblock, admonition = reformat_line(line2, codeblock, admonition, 1)
                            readme_content.append(line2)
            else:
                line1, codeblock, admonition = reformat_line(line1, codeblock, admonition, 0)
                readme_content.append(line1)

    with open(output_file, 'w') as file:
        file.writelines(readme_content)


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_readme(input_file, output_file)
