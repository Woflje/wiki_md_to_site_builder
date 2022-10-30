from conv.format import format_hr, format_list, format_code, format_table
from conv.convert import convert_line
import os

ul_bullets = [
	"&#8226;",
	"&#8259;"
]

def md_to_html(md_path, html_path):
    print(f"[Wiki Reader Builder] Converting {md_path} to Mark Down code")
    md_html = "<br>\n"
    with open(md_path, 'r') as mdf:
        mds = mdf.read()
        lines = mds.split('\n')
        fl = True                   # First Line

        list_depth = 0
        clp = ""                    # Current Line Prefix
        plp = ""                    # Previous Line Prefix
        in_list = None

        cb = False                  # Code Block
        cbt = False                 # Code Block Indent
        co = 0                      # Nr of Code Block Opened
        
        i = 0
        while i < len(lines):
            line = lines[i]
            br = "<br>"
            # Check for Horizontal Line
            if format_hr(line):
                md_html += f"<hr>\n"
                i+=1
                continue

            # Check for Lists
            in_list, list_depth, clp, plp = format_list(line, list_depth, clp, plp)

            # Check for code and code blocks
            md_html, line, cb, cbt, co, br = format_code(md_html, line, cb, cbt, co, in_list, br)

            if not cb and len(line) > 0:
                if '|' in line and i < len(lines) - 1:
                    i, table, md_html = format_table(i, lines, md_html)
                    if table:
                        table = False
                        i+=1
                        continue
            if not cb and '`' not in lines[i]:
                line = convert_line(line)

            if len(line) > 1 and line[-1] == '\\' and not cb:
                line = line.split('\\',-1)[0]
            
            if in_list == "UL":
                line = line.replace('-', ul_bullets[list_depth%len(ul_bullets)], 1)
            
            if in_list is not None:
                q = list_depth + 1
            else:
                q = 0

            if fl:
                md_html += f'{"&nbsp;"*4*q}{line}{br}\n'
                fl = False
            else:
                md_html += f'{"&nbsp;"*4*q}{line}{br}\n'

            i+=1

    md_html += "<br>\n"*4
    html_path = html_path.replace(' ','_')
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, 'w') as htmlf:
        htmlf.write(md_html)