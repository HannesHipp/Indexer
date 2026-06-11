def export_log(removed_words: dict[str, tuple[list[list[int]], list[int], str]]) -> None:
    with open("log.txt", "w+") as o:

        max_word_len = max((len(word) for word in removed_words), default=4)
        max_reason_len = max((len(reason) for _, (_, _, reason) in removed_words.items()), default=6)
        max_groups_len = max((len(format_groups(groups)) for _, (groups, _, _) in removed_words.items()), default=6)
        max_outliers_len = max((len(format_outliers(outliers)) for _, (_, outliers, _) in removed_words.items()), default=8)

        header = f"{'Word'.ljust(max_word_len)}  {'Reason'.ljust(max_reason_len)}  {'Groups'.ljust(max_groups_len)}  {'Outliers'.ljust(max_outliers_len)}\n"
        o.write(header)
        o.write("-" * len(header) + "\n")

        for word, (groups, outliers, reason) in removed_words.items():
            groups_str = format_groups(groups)
            outliers_str = format_outliers(outliers)
            line = f"{word.ljust(max_word_len)}  {reason.ljust(max_reason_len)}  {groups_str.ljust(max_groups_len)}  {outliers_str.ljust(max_outliers_len)}\n"
            o.write(line)

def format_groups(groups: list[list[int]]) -> str:
    return "|".join(f"{group[0]}-{group[-1]}" if len(group) > 1 else f"{group[0]}" for group in groups)

def format_outliers(outliers: list[int]) -> str:
    return ",".join(map(str, outliers)) if outliers else "-"