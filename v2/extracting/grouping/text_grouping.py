from extracting.grouping.block_grouping import lines_match

def get_line_text(line):
    return ' '.join([span['text'] for span in line['spans']])

def get_text_groups(block_groups):
    text_groups = []
    current_group = ''

    for block_group in block_groups:
        last_line = None
        for block in block_group:
            for current_line in block['lines']:
                if last_line and not lines_match(last_line, current_line):
                    text_groups.append(current_group.strip())
                    current_group = ''
                current_group += ' ' + get_line_text(current_line)
                last_line = current_line
        if current_group:
            text_groups.append(current_group.strip())
            current_group = ''

    return text_groups