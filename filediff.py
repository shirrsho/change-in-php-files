import difflib

def count_sloc(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sloc_count = 0
    in_multiline_comment = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("#"):
            continue

        if line.startswith("/*"):
            in_multiline_comment = True

        if line.endswith("*/"):
            in_multiline_comment = False
            continue

        if in_multiline_comment:
            continue

        sloc_count += 1

    return sloc_count

def compare_php_files(file_path1, file_path2):

    with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    d = difflib.Differ()
    diff = d.compare(lines1, lines2)

    lines_added = 0
    lines_removed = 0
    lines_modified = 0


    for line in diff:
        if line.startswith('? '):
            if line.strip():
                lines_modified += 1
        elif line.startswith('+ '):
            lines_added += 1
        elif line.startswith('- '):
            lines_removed += 1

    return lines_added, lines_removed, lines_modified

if __name__ == "__main__":
    php_file_path1 = "cwslack-configs.php"
    php_file_path2 = "cwslack-configs-v2.php"

    lines_added, lines_removed, lines_modified = compare_php_files(php_file_path1, php_file_path2)
    sloc_diff = count_sloc(php_file_path2) - count_sloc(php_file_path1)

    print(f"Sloc Diff: {sloc_diff}")
    print(f"Lines added: {lines_added}")
    print(f"Lines removed: {lines_removed}")
    print(f"Lines modified: {lines_modified}")