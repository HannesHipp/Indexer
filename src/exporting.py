def export_index(index, slides_per_page, removed_words):
    for word in index:
        page_numbers = []
        for slide in index[word]:
            if slides_per_page > 1:
                num = update_page_numbers(slide.global_slide_num, slides_per_page)
            else:
                num = str(slide.global_slide_num)
            page_numbers.append(num)
        index[word] = ", ".join(sorted(page_numbers))

    index = sort_index(index)
    html = create_html(index)

    with open("output.html", "w+") as o:
            o.write(html)

    with open("removed.txt", "w+") as o:
        for word in removed_words:
            o.write(f"{word}\n")

def update_page_numbers(old_page_number, slides_per_page):
    main_page = (old_page_number - 1) // slides_per_page + 1
    sub_page = (old_page_number - 1) % slides_per_page + 1
    return f"{main_page}-{sub_page}"

def sort_index(my_dict):
    def normalize_key(key):
        key = key.lower()
        key = key.replace('ä', 'a')
        key = key.replace('ö', 'o')
        key = key.replace('ü', 'u')
        return key

    sorted_dict = dict(sorted(my_dict.items(), key=lambda item: normalize_key(item[0])))
    return sorted_dict

def create_html(index):
    content = """
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
    """
    
    current_letter = ''
    
    for word in index.keys():

        first_letter = word[0].upper()
        
        if first_letter != current_letter:
            current_letter = first_letter
            content += f'<p style="font-size:40px;"><b>{current_letter}</b></p>'
        
        pages = index[word]
        content += f'<p style="font-size:16px;"><b>{word}</b>: {pages}</p>'
    
    content += """
    </body>
    </html>
    """
    
    return content
