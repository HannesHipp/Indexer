def generate_index(words, output_path, grouping):
    index = {}
    for word in words:
        page_numbers = []
        for slide in words[word]:
            page_numbers.append(slide.slide_number)
        index[word] = page_numbers
    index = dict(sorted(index.items()))
    with open("output.txt", "w+") as o:
        for word in index:
            o.write(f"{word}: {str(index[word])}\n")
