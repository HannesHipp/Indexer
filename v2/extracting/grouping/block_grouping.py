import fitz  # PyMuPDF

def get_block_corners(block, left, upper):
    x0, y0, x1, y1 = block["bbox"]
    if left:
        if upper:
            return (x0, y0)
        else:
            return (x0, y1)
    else:
        if upper:
            return (x1, y0)
        else:
            return (x1, y1)

def get_line_height(block):
    last_line = block["lines"][-1]
    return last_line["bbox"][3] - last_line["bbox"][1]

def get_char_width(block):
    last_line = block["lines"][-1]
    last_span = last_line["spans"][-1]
    text = last_span["text"]
    num_chars = max(len(text), 1)  # Avoid division by zero
    return (last_span["bbox"][2] - last_span["bbox"][0]) / num_chars  # Approximate width

def lines_match(line1, line2):
    return bool(get_formats(line1).intersection(get_formats(line2)))

def get_formats(line):
    return set([(span['font'], span['size'], span['color']) for span in line['spans']])

def get_block_groups(page):
    blocks = [b for b in page.get_text("dict")["blocks"] if "lines" in b and b["lines"]]
    blocks.sort(key=lambda b: get_block_corners(b, left=True, upper=True)[1])  # Sort by top-left y-coordinate
    block_groups = []
    while blocks:
        upper_block = blocks.pop(0)  # Take the first block
        current_group = [upper_block]
        line_height = get_line_height(upper_block)
        vertical_threshold = 0.5 * line_height
        char_width = get_char_width(upper_block)
        horizontal_threshold = 15 * char_width
        remove_blocks = []
        for lower_block in blocks:
            up_left_x, up_bot_y = get_block_corners(upper_block, left=True, upper=False)
            low_left_x, low_top_y = get_block_corners(lower_block, left=True, upper=True)
            # Ensure current_box is actually below top_box
            ver_dist = low_top_y - up_bot_y
            if ver_dist < 0:
                continue
            # Stop iterating if the vertical distance is too large
            if ver_dist > vertical_threshold:
                break
            # Check horizontal proximity
            hor_dist = low_left_x - up_left_x
            if abs(hor_dist) > horizontal_threshold:
                continue
            # Check formatting consistency
            if lines_match(upper_block['lines'][-1], lower_block['lines'][0]):
                current_group.append(lower_block)
                remove_blocks.append(lower_block)
                upper_block = lower_block
            else:
                break
        blocks = [b for b in blocks if b not in remove_blocks]
        block_groups.append(current_group)
    return block_groups





def vizualize_block_groups(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)

    page_number = 1
    for page in doc:
        grouped_blocks = get_block_groups(page)

        # Draw individual block rectangles (green)
        for group in grouped_blocks:
            for block in group:
                page.draw_rect(block["bbox"], color=(0, 1, 0), width=0.5)  # Green

        # Draw grouped block rectangles (red)
        for group in grouped_blocks:
            min_x = min(block["bbox"][0] for block in group)
            min_y = min(block["bbox"][1] for block in group)
            max_x = max(block["bbox"][2] for block in group)
            max_y = max(block["bbox"][3] for block in group)

            page.draw_rect((min_x, min_y, max_x, max_y), color=(1, 0, 0), width=1)  # Red
        page_number += 1

    # Save output
    doc.save(output_pdf)
    doc.close()

# vizualize_block_groups(r'ressources/Skript.pdf', 'output.pdf')