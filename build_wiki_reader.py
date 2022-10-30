from conv.md_to_html import md_to_html
import os

nav = {
    "folders": {},
    "files": []
}

def build_wiki_reader(html_base_path, wiki_md_path, wiki_path, home_file_name):
    with open(html_base_path, 'r') as html_base_file:
        html_base = html_base_file.read()
    for folderName, subfolders, filenames in os.walk(wiki_md_path):
        for filename in filenames:
            filePath = os.path.join(folderName,filename)
            if filename.endswith('.md'):
                html_file_name = f'{filename.split(".",-1)[0]}.html'
                html_folder_name = f'{wiki_path}{folderName.split(wiki_md_path)[1]}'
                html_file_path = os.path.join(html_folder_name,html_file_name)
                md_to_html(filePath, html_file_path)
                add_nav(html_file_path, wiki_path)
    for line in html_base.split('\n'):
        if 'wolfs_md_to_html_nav_placeholder' in line:
            indent = line.split('wolfs_md_to_html_nav_placeholder')[0]
        if 'wolfs_md_to_html_open_with_file_placeholder' in line:
            prefix_ = line.split('wolfs_md_to_html_open_with_file_placeholder')[0]
            break
    nav_html = add_nav_folder(nav, indent, 0, wiki_path)
    html = html_base.replace(f'{indent}wolfs_md_to_html_nav_placeholder', nav_html)
    html = html.replace(f'{prefix_}wolfs_md_to_html_open_with_file_placeholder;', f'{prefix_}"{home_file_name}";')
    with open(f'{wiki_path}index.html','w') as f:
        f.write(html)

def add_nav(html_file_path, root):
    subfolders = html_file_path.split(root)[-1].split('\\')
    if len(subfolders) > 0:
        tnav = nav
        for s in range(0,len(subfolders)-1):
            subfolder = subfolders[s]
            if subfolder not in tnav['folders']:
                tnav = tnav['folders']
                tnav[subfolder] = {
                    "folders": {},
                    "files": []
                }
                tnav = tnav[subfolder]
            else:
                tnav = tnav['folders'][subfolder]
        tnav['files'].append(html_file_path)

def add_nav_folder(nav_folder, indent, depth, root, folder_path=None):
    style=f'style="margin-left: {str((depth)*10)}px" '
    folder_html = ''
    if folder_path is not None:
        folder_path = folder_path.replace("\\", "__")
        folder_name = folder_path.split('__',-1)[-1]
        folder_path = folder_path.replace(" ", "_")
        folder_html += f'{indent}<div {style}class="nav_button nav_folder" onclick="toggle_nav_folder('+f"'folder_name_{folder_path}'"+f')">{folder_name}</div>\n'
        folder_html += f'{indent}<div class="nav_folder_container" id="folder_name_{folder_path}">\n'
    for folder in nav_folder['folders']:
        if folder_path is not None:
            fp = f'{folder_path}\\{folder}'
        else:
            fp = folder
        folder_html += add_nav_folder(nav_folder['folders'][folder], indent+'    ', depth+1, root, fp)
    style=f'style="margin-left: {str((depth+1)*10)}px" '
    root = root.replace('\\', '\\\\')
    for file in nav_folder['files']:
        file = file.replace('\\', '\\\\')
        file_name = file.split(".",-1)[0].split("\\\\",-1)[-1]
        file = file.replace(' ', '_')
        file_ = file.split(root)[-1].replace('.html','').replace('\\\\','__')
        folder_html += f'{indent}<div {style}class="nav_button nav_file" id="{file_}" onclick="load_wiki_chapter('+f"'{file.split(root)[-1]}'"+f')">{file_name}</div>\n'
    if folder_path is not None:
        folder_html += f'{indent}</div>\n'
    return folder_html