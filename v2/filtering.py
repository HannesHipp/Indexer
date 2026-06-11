

class IndexFilter:

    def __init__(self, gap_percentage: float, max_group_range: int, max_outliers: int, max_total: int):
        self.gap_percentage = gap_percentage
        self.max_group_range = max_group_range
        self.max_outliers = max_outliers
        self.max_total = max_total

    def filter_index(self, index: dict[str, dict[str, dict[int, int]]], number_of_slides: int):
        result = {}
        removed_words = {}
        for noun, adjectives in index.items():
            for adjective, occurrence in adjectives.items():
                groups, outliers = self.group_slides(list(occurrence.keys()), number_of_slides)
                valid_grouping, removal_reason = self.is_valid_grouping(groups, outliers)
                if valid_grouping:
                    if noun not in result:
                        result[noun] = {}
                    result[noun][adjective] = (groups, outliers)
                else:
                    combined_word = f"{adjective} {noun}"
                    removed_words[combined_word] = (groups, outliers, removal_reason)
        return result, removed_words

    def group_slides(self, slides, number_of_slides):
        max_distance = int(number_of_slides * self.gap_percentage)
        slides.sort()
        groups = []
        outliers = []
        current_group = [slides[0]]

        for i in range(1, len(slides)):
            if slides[i] - current_group[-1] <= max_distance:
                current_group.append(slides[i])
            else:
                if len(current_group) <= 2:
                    outliers.extend(current_group)
                else:
                    groups.append(current_group)
                current_group = [slides[i]]
        if len(current_group) <= 2:
            outliers.extend(current_group)
        else:
            groups.append(current_group)
        return groups, outliers
    
    def is_valid_grouping(self, groups, outliers):
        if len(outliers) > self.max_outliers:
            return False, f"Outliers: {len(outliers)} > {self.max_outliers}"

        total_numbers = sum(len(group) for group in groups)
        if total_numbers > self.max_total:
            return False, f"Total pages: {total_numbers} > {self.max_total}"

        for group in groups:
            max_page_num = max(group)
            min_page_num = min(group)
            group_range = max_page_num - min_page_num
            if group_range > self.max_group_range:
                return False, f"Group range [{min_page_num} - {max_page_num}] = {group_range} > {self.max_group_range}"

        return True, None


# import matplotlib.pyplot as plt
# import numpy as np

# def compute_gaps(word_data, number_of_slides):
#     """Compute sorted gap lengths for a word's page occurrences."""
#     pages = sorted(word_data.keys())
#     pages.append(number_of_slides + 1)
#     pages = [0] + pages  # Add a 0 at the beginning for the first gap
#     gaps = []
#     for i in range(1, len(pages)):
#         gaps.append(pages[i] - pages[i-1] - 1)
#     return [gap for gap in gaps if gap != 0]

# def visualize_gaps(word_dict, number_of_slides, output_file="word_gaps.png"):
#     """Visualize gaps and occurrence plots for the top 5 and bottom 5 words based on total occurrences."""
#     total_counts = {word: sum(pages.values()) for word, pages in word_dict.items()}
#     sorted_words = sorted(total_counts, key=total_counts.get)
#     selected_words = sorted_words[:5] + sorted_words[-5:]  # 5 lowest + 5 highest
    
#     fig, axes = plt.subplots(len(selected_words), 2, figsize=(12, 4 * len(selected_words)))
    
#     for i, word in enumerate(selected_words):
#         gaps = compute_gaps(word_dict[word], number_of_slides)
#         pages = sorted(word_dict[word].keys())
#         occurrences = [word_dict[word][p] for p in pages]
        
#         # Gap plot
#         ax1 = axes[i, 0]
#         if gaps:
#             y_pos = np.arange(len(gaps))
#             ax1.barh(y_pos, gaps, align='center')
#             ax1.set_yticks(y_pos)
#             ax1.set_yticklabels([f'Gap {j+1}' for j in range(len(gaps))])
#             ax1.set_xlabel('Gap Length')
#             ax1.set_title(f'Page Gaps for "{word}"')
#             ax1.invert_yaxis()
        
#         # Occurrence plot
#         ax2 = axes[i, 1]
#         ax2.bar(pages, occurrences, align='center')
#         ax2.set_xticks(pages)
#         ax2.set_xlabel('Page Number')
#         ax2.set_ylabel('Occurrences')
#         ax2.set_title(f'Occurrences of "{word}"')
    
#     plt.tight_layout()
#     plt.savefig(output_file, dpi=300)
#     plt.close()