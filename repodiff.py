import os
import difflib

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

def find_added_removed_lines(folder1, folder2):
    added_lines = {}
    removed_lines = {}

    for root, _, files in os.walk(folder1):
        for file in files:
            if file.endswith(".php"):
                file_path1 = os.path.join(root, file)
                relative_path = os.path.relpath(file_path1, folder1)
                file_path2 = os.path.join(folder2, relative_path)

                if os.path.exists(file_path2):
                    lines_added, lines_removed, added_line_numbers = compare_php_files(file_path1, file_path2)
                    if lines_added > 0:
                        added_lines[relative_path] = added_line_numbers
                    if lines_removed > 0:
                        removed_lines[relative_path] = lines_removed

    return added_lines, removed_lines

if __name__ == "__main__":
    folder1_path = "folder1"
    folder2_path = "folder2"

    added_lines, removed_lines = find_added_removed_lines(folder1_path, folder2_path)

    print("Added lines:")
    for file_path, lines_added in added_lines.items():
        print(f"File: {file_path}")
        for line_number, line_content in lines_added.items():
            print(f"Line {line_number}: {line_content.strip()}")

    print("\nRemoved lines:")
    for file_path, lines_removed in removed_lines.items():
        print(f"File: {file_path}, Removed lines: {lines_removed}")