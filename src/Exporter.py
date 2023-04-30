import openpyxl
from openpyxl.utils import get_column_letter

class IndexExporter:

    def __init__(self) -> None:
        pass

    def generate_index(self, words, output_path, grouping):
        index = self.create_index(words)
        self.generate_word_index(index, output_path)

    def create_index(self, words):
        index = {}
        for word in words:
            page_numbers = []
            for slide in words[word]:
                page_numbers.append(slide.global_slide_num)
            index[word] = page_numbers
        return dict(sorted(index.items()))

    def generate_word_index(self, index, output_path):
        # Create a new Excel workbook and add a worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Set the column width
        column_width = 20
        for col_num in range(1, 5):
            column_letter = get_column_letter(col_num)
            sheet.column_dimensions[column_letter].width = column_width

        # Write the index to the worksheet
        row = 1
        col = 1
        for word, page_numbers in index.items():
            line = f"{word}: {', '.join(map(str, page_numbers))}"
            sheet.cell(row=row, column=col, value=line)

            # Move to the next cell
            col += 1
            if col > 4:
                col = 1
                row += 1

        # Save the workbook
        workbook.save(output_path)