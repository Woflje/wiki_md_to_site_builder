from conv.convert import convert_line

numbers = list(range(0,10))
for i in range(0,len(numbers)):
    numbers[i] = str(numbers[i])

def format_hr(line):
    if len(line) > 2 and line == "-"*len(line):
        return True
    return False

def get_list_depth(nlp, clp, u):
    if len(clp) < len(nlp):
        u+=1
    elif len(clp) > len(nlp):
        u-=1
    return clp, nlp, u

def format_list(line, u, plp, clp):
    if len(line) > 0:
        for i in range(0, len(line)):
            if line[i] == '-':
                if i != len(line)-1:
                    if line[i+1] == ' ':
                        plp, clp, u = get_list_depth(line[0:i], clp, u)
                        in_list = "UL"
                        break
            elif line[i] in numbers:
                j = i+1
                while j < len(line) -1:
                    if line[j] in numbers:
                        j+=1
                    elif line[j] == '.':
                        plp, clp, u = get_list_depth(line[0:i], clp, u)
                        in_list = "OL"
                        break
                break
            elif line[i] != ' ':
                in_list = None
                u = 0
                break
    else:
        in_list = None
        u = 0
        clp = ""
        plp = ""
    return in_list, u, clp, plp

def format_code(md_html, line, cb, cbt, co, in_list, br):
    if '`' in line:
        if cb:
            if '`'*co in line or (cbt and line[0] != '\t'):
                line = '</div>'
                br = ""
                cb = False
            else:
                line = convert_line(line, 'code')
        else:
            c = 0
            if line[0] == '`' and line[-1] == '`':
                cb = True
                for i in range(0, len(line)):
                    if line[i] != '`':
                        cb = False
                        break
            elif in_list is None and line[0] == '\t':
                md_html += f'<div class="code_block">\n'
                br = ""
                cb = True
                cbt = True
            if cb:
                co = len(line)
                line = '<div class="code_block">'
                br = ""
            if not cb:
                tline = line
                while '`' in tline:
                    nline = convert_line(line.split('`',1)[0])
                    c = 0
                    for x in tline:
                        if x == '`':
                            c+=1
                        elif c > 0:
                            if '`'*c in line.split('`'*c,1)[1]:
                                incode_line = convert_line(tline.split("`"*c,2)[1], 'code')
                                nline += f'<span class="inline_code">{incode_line}</span>'
                            break
                    tline = tline.split('`'*c,2)[2]
                nline += convert_line(tline)
                line = nline
    return md_html, line, cb, cbt, co, br

def get_table_td(tl):
    if tl[0] == '|':
        tl = tl[1:]
    if tl[-1] == '|':
        tl = tl[:-1]
    return tl.split('|')

def format_table(i, lines, md_html):
    thl = lines[i]
    tfli = i+1
    tfl = lines[tfli]
    table = False
    if '|' in tfl and len(thl) > 0:
        th = get_table_td(thl)
        tf = get_table_td(tfl)
        if len(th) == len(tf):
            table = True
            md_html += "<table>\n<thead>\n<tr>\n"
            for t in th:
                md_html += f"<td>{convert_line(t)}</td>\n"
            md_html += "</tr>\n</thead>\n"
            i = i+2
            j = i
            while i < len(lines) and '|' in lines[i]:
                if i == j:
                    md_html += "<tbody>\n"
                md_html += "<tr>\n"
                td = get_table_td(lines[i])
                for t in range(0, len(th)):
                    md_html += f"<td>{convert_line(td[t])}</td>\n"
                md_html += "</tr>\n"
                i += 1
            if j != i:
                md_html += "</tbody>\n"
    return i, table, md_html