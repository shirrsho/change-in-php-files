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
        
        print(line)

    return sloc_count

if __name__ == "__main__":
    php_file_path = "cwslack-configs.php"
    sloc_count = count_sloc(php_file_path)
    print(f"SLOC: {sloc_count}")