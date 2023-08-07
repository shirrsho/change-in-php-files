import os
import difflib

def compare_php_files(file_path1, file_path2):

    with open(file_path1, 'r', encoding="utf-8") as file1, open(file_path2, 'r', encoding="utf-8") as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    d = difflib.Differ()
    diff = d.compare(lines1, lines2)

    lines_added = 0
    lines_removed = 0


    for line in diff:
        if line.startswith('+ '):
            lines_added += 1
        elif line.startswith('- '):
            lines_removed += 1

    return { 'added':lines_added, 'removed':lines_removed }

def find_matching_files(folder1, folder2):
    matching_files = []
    changed = []

    for root1, _, files1 in os.walk(folder1):
        for root2, _, files2 in os.walk(folder2):
            for file1 in files1:
                if file1 in files2:
                    if str(os.path.join(root1,file1)).replace("folder1", "") != str(os.path.join(root2,file1)).replace("folder2", ""):
                        continue
                    # matching_files.append(os.path.join(root1, file1))
                    # matching_files.append(os.path.join(root2, file1))
                    if not str(file1).endswith('.php'):
                        continue
                    # print(os.path.join(root2,file1))
                    changes = compare_php_files(os.path.join(root1,file1),os.path.join(root2, file1))
                    if changes['added'] == 0 and changes['removed'] == 0:
                        continue
                    changes['file'] = os.path.join(root1,file1)
                    changes['changed'] = changes['added'] + changes['removed']
                    changed.append(changes)
                    # print(changes['file'],'{')
                    # print('\tadded: ',changes['added'])
                    # print('\tremoved: ',changes['removed'])
                    # print('\tchanged: ',changes['changed'])
                    # print('}')
    
    return changed

if __name__ == "__main__":
    folder1 = "folder1"
    folder2 = "folder2"

    changed = find_matching_files(folder1, folder2)
    total = {
        'added':0,
        'removed':0,
        'changed':0
    }

    if changed:
        print("Changes:")
        for change in changed:
            print(change['file'],'{')
            print('\tadded: ',change['added'])
            print('\tremoved: ',change['removed'])
            print('\tchanged: ',change['changed'])
            print('}')
            total = {
                'added':total['added']+change['added'],
                'removed':total['removed']+change['removed'],
                'changed':total['changed']+change['changed'],
            }
        print('Total changes: ')
        print('{')
        print('\tadded: ',total['added'])
        print('\tremoved: ',total['removed'])
        print('\tchanged: ',total['changed'])
        print('}')
    else:
        print("No changes in files found.")
        
    