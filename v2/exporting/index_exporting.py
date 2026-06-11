def export_index(index: dict[str, dict[str, tuple[list[list[int]], list[int]]]], slides_per_page):
    # Iterate over each noun in the index
    for noun, adjectives in index.items():
        # Iterate over each adjective under the noun
        for adjective, (groups, outliers) in adjectives.items():
            main_sub_mapping = {}
            
            # Flatten the groups and combine with outliers
            all_pages = [page for group in groups for page in group] + outliers
            
            # Combine and sort the page numbers
            for page_num in sorted(set(all_pages)):
                main_page = (page_num - 1) // slides_per_page + 1
                sub_page = (page_num - 1) % slides_per_page + 1
                
                if main_page not in main_sub_mapping:
                    main_sub_mapping[main_page] = []
                main_sub_mapping[main_page].append(sub_page)
            
            # Update the index with the new page mapping for this adjective under the noun
            index[noun][adjective] = main_sub_mapping
    
    # Generate the HTML content
    html = create_html(index)

    # Write to the HTML file
    with open("output.html", "w+") as o:
        o.write(html)


def create_html(index):
    content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            table { border-collapse: collapse; width: 100%; }
            td { padding: 2px; vertical-align: top; }
        </style>
    </head>
    <body>
    <table>
    """

    current_letter = ''
    
    def normalize_key(key):
        return key.lower().replace('ä', 'a').replace('ö', 'o').replace('ü', 'u')

    for noun, adjectives in sorted(index.items(), key=lambda item: normalize_key(item[0])):
        first_letter = noun[0].upper()
        
        if first_letter != current_letter:
            current_letter = first_letter
            content += f'<tr><td colspan="2" style="font-size:40px;"><strong>{current_letter}</strong></td></tr>'
        
        # Process noun and directly attached pages
        noun_main_pages = ""
        formatted_adjectives = []

        for adjective, pages_dict in sorted(adjectives.items(), key=lambda item: normalize_key(item[0])):
            formatted_pages = " ".join(
                f"{main_page}[{'|'.join(map(str, sorted(subpages)))}]"
                for main_page, subpages in sorted(pages_dict.items())
            )

            if adjective == "":  
                noun_main_pages = formatted_pages  # Attach to the noun row
            else:
                formatted_adjectives.append(
                    f'<tr><td style="width: 10%;"></td><td style="width: 90%;"><strong>{adjective}</strong>: {formatted_pages}</td></tr>'
                )

        # Row for the noun (Single column but spans both columns)
        content += f'<tr><td colspan="2" style="font-size:16px;"><strong>{noun}</strong>: {noun_main_pages}</td></tr>'

        # Insert all adjective rows (Two-column structure)
        content += "".join(formatted_adjectives)

    content += """
    </table>
    </body>
    </html>
    """

    return content
