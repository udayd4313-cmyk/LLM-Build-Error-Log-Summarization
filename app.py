"""Command-line interface for build and error log summarization."""

from datetime import datetime
from pathlib import Path

from log_analyzer import analyze_log
from summarizer import SummarizationError, generate_summary


PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"


def resolve_log_path(user_input: str) -> Path:
    """Resolve absolute paths or paths relative to the project directory."""
    path = Path(user_input.strip().strip('"')).expanduser()
    if not path.is_absolute():
        path = PROJECT_DIR / path
    return path


def save_summary(log_path: Path, summary: str) -> Path:
    """Save a summary in output/ with a unique timestamped filename."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = OUTPUT_DIR / f"{log_path.stem}_summary_{timestamp}.txt"
    output_path.write_text(summary.rstrip() + "\n", encoding="utf-8")
    return output_path


def analyze_file(user_input: str) -> None:
    """Read, analyze, summarize, and save one log file."""
    try:
        log_path = resolve_log_path(user_input)
        if not log_path.exists():
            print(f"Error: file not found: {log_path}")
            return
        if not log_path.is_file():
            print(f"Error: the selected path is not a file: {log_path}")
            return
        log_text = log_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Error: could not read the log file: {error}")
        return

    try:
        analysis = analyze_log(log_text)
        summary = generate_summary(log_text, analysis)
        saved_path = save_summary(log_path, summary)
    except SummarizationError as error:
        print(f"Could not generate the AI summary: {error}")
        return
    except OSError as error:
        print(f"Error: could not save the summary: {error}")
        return

    print("\n" + "=" * 72)
    print("BUILD LOG SUMMARY")
    print("=" * 72)
    print(summary)
    print("=" * 72)
    print(f"Summary saved to: {saved_path}")


def main() -> None:
    """Run the interactive command-line application."""
    print("Welcome to the LLM-Based Build/Error-Log Summarization tool!")
    print("Enter a log file path (absolute or relative to this project).")

    while True:
        try:
            log_path = input("\nLog file path (or 'q' to quit): ").strip()
            if log_path.lower() in {"q", "quit", "exit"}:
                print("Goodbye.")
                break
            if not log_path:
                print("Please enter a file path.")
                continue

            analyze_file(log_path)
            again = input("\nAnalyze another log? (y/n): ").strip().lower()
            if again not in {"y", "yes"}:
                print("Goodbye.")
                break
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()