from .index_exporting import export_index
from .log_exporting import export_log


def export_data(index, slides_per_page, removed_words):
    export_log(removed_words)
    export_index(index, slides_per_page)