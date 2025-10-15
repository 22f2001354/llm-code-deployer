import os
import shutil
import stat

def remove_readonly(func, path, excinfo):
    # Clear read-only attribute and retry
    os.chmod(path, stat.S_IWRITE)
    func(path)

def generate_app_code(brief, task_name):
    folder_path = os.path.join("temp_app")
    
    # Remove existing folder to start fresh
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path, onerror=remove_readonly)
    os.makedirs(folder_path, exist_ok=True)

    # Create basic files for Markdown-to-HTML app
    with open(os.path.join(folder_path, "index.html"), "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Markdown to HTML</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
<textarea id="markdown" rows="10" cols="50"># Hello Markdown</textarea>
<div id="html"></div>
<script>
const md = document.getElementById('markdown');
const html = document.getElementById('html');
md.addEventListener('input', () => {
    html.innerHTML = marked.parse(md.value);
});
</script>
</body>
</html>""")

    with open(os.path.join(folder_path, "README.md"), "w") as f:
        f.write(f"# {task_name}\nThis is a Markdown-to-HTML converter using marked.js.")

    with open(os.path.join(folder_path, "LICENSE"), "w") as f:
        f.write("MIT License")

    return folder_path
