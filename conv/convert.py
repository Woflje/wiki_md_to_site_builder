numbers = list(range(0,10))
for i in range(0,len(numbers)):
    numbers[i] = str(numbers[i])

html_codes = {
    '&': '&#38;',
    '#': '&#35;',
    '<': '&#60;',
    '>': '&#62;'
}

def convert_header(line):
    suffix = '</div>'
    if line[0:2] == '# ':
        return '<div class="h">', line.split("# ")[1], suffix
    elif line[0:3] == '## ':
        return '<div class="hh">', line.split("## ")[1], suffix
    elif line[0:4] == '### ':
        return '<div class="hhh">', line.split("### ")[1], suffix
    else:
        return '', line, ''

def convert_symbols(line, code=False):
    nline = ""
    if code:
        for x in line:
            if x in html_codes:
                nline += html_codes[x]
            else:
                nline += x
    else:
        s = 0
        for i in range(0,len(line)):
            if s > 0:
                s -= 1
            else:
                if line[i] == '#':
                    nline += html_codes['#']
                elif line[i] == '&':
                    amp = True
                    if i < len(line)-1:
                        if line[i+1] == '#':
                            j = i + 2
                            while j < len(line):
                                if line[j] in numbers:
                                    j+=1
                                elif j > i+2 and line[j] == ';':
                                    amp = False
                                    nline += line[i:j+1]
                                    s = j+1-i
                                    break
                                else:
                                    break
                    if amp:
                        nline += html_codes['&']
                else:
                    nline += line[i]
    return nline

def convert_url(line):
    while '](' in line:
        s1 = line.split('](',1)
        s2 = s1[0].split('[',-1)
        label = s2[1]
        link = s1[1].split(')',1)[0]
        line = f'{s2[0]}<a href="{link}">{label}</a>{s1[1].split(")",1)[1]}'
    return line

def convert_line(line, mode='normal'):
    if mode == 'normal':
        prefix, line, suffix = convert_header(line)
        line = convert_symbols(line)
        line = convert_url(line)
        line = f'{prefix}{line}{suffix}'
    elif mode == 'code':
        line = convert_symbols(line, True)
    return line