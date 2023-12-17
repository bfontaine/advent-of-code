from colorama import init, Style

init()

__all__ = ["colored_text", "c"]


def colored_text(text: str, *colors: str):
    return f"{''.join(colors)}{text}{Style.RESET_ALL}"


c = colored_text
