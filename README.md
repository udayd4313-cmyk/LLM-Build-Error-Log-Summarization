# LLM-Based Build/Error-Log Summarization

## Project introduction

This command-line project uses deterministic log analysis and the Groq API to
turn build output into a readable summary. It is designed as a beginner-friendly
Python assignment and includes sample failed and successful build logs.

## Problem statement

Build logs can be long and difficult to interpret. Developers may need to find
the first meaningful error, understand whether a build completed, and decide
what to investigate next. This tool highlights log levels locally and asks an
LLM to explain the evidence in plain language.

## Objectives

- Read a user-selected UTF-8 build log.
- Count `ERROR`, `WARNING`, `FATAL`, and `INFO` messages.
- Detect common build failure indicators and extract important lines.
- Generate an evidence-based summary with Groq.
- Save each successful summary as a timestamped text file.

## Features

- Interactive command-line interface with repeat-analysis support.
- Relative and absolute log file paths.
- Deterministic message counts, error extraction, and build status hints.
- AI-generated explanations covering status, errors, possible causes,
  suggestions, and warnings.
- Clear handling of invalid paths, missing API keys, and API errors.
- Summary files saved under `output/`.

## Technologies used

- Python 3.10 or later
- Groq Python SDK (`groq`)
- `python-dotenv`
- Python standard library (`pathlib`, `datetime`, `re`, and `collections`)

## Project structure

```text
LLM-Build-Error-Log-Summarization/
├── sample_logs/
│   ├── build_error.log
│   └── successful_build.log
├── output/
│   └── .gitkeep
├── screenshots/
│   └── .gitkeep
├── app.py
├── summarizer.py
├── log_analyzer.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Generated summary files are added to `output/`; the `screenshots/` directory is
reserved and remains empty.

## Installation

Open a terminal in the project directory and install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

If you use a virtual environment, activate it before installing. For example,
on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

## Groq API key configuration

1. Copy `.env.example` to a new file named `.env` in the project root.
2. Replace the placeholder value for `GROQ_API_KEY` with your own Groq API key.
3. Optionally change `GROQ_MODEL`; the default is `llama-3.3-70b-versatile`.
4. Keep `.env` private. It is excluded from Git by `.gitignore`.

The application never prints or stores the API key in generated summaries.
Without a configured key or if the API call fails, it reports the error and does
not create a fabricated summary.

## How to execute the application

Run the CLI from the project directory:

```powershell
python app.py
```

Enter an absolute path or a path relative to the project root, such as
`sample_logs/build_error.log`. Review the generated summary and the path to its
timestamped file in `output/`. Choose `y` when prompted to analyze another log,
or `n` to exit.

## Sample input and output

Sample input: `sample_logs/build_error.log`. It contains a dependency resolution
problem, a source compilation error, a warning, and a final build failure.

The deterministic analysis will report a likely failed build and counts for
the detected message levels. A successful Groq response will have this general
shape (the actual wording depends on the log and model):

```text
Overall build status
Likely failed: the log reports BUILD FAILED and a non-zero exit code.

Main errors
Dependency resolution failed and compilation reported invalid syntax.

Possible root causes
The requested dependency version is unavailable; the source has a syntax
error. The log does not establish why either issue was introduced.

Suggested solutions
Check the dependency version against available releases and inspect the
reported source line for the missing syntax.

Important warnings
The log reports an unused variable and an optional package that was skipped.
```

The exact output is generated from the real API response and is never replaced
with a canned answer if the API is unavailable.

## Learning outcomes

- Reading files and handling paths with `pathlib`.
- Separating CLI, log-analysis, and API responsibilities across modules.
- Extracting structured information using regular expressions.
- Managing API credentials with environment variables.
- Handling file and network/API errors.
- Working with structured chat-completion requests and saving output files.

## Limitations and future improvements

- Failure detection uses a small set of text patterns and may miss tool-specific
  status formats.
- Large logs may exceed model context limits; the current version sends the
  complete log.
- The AI summary depends on network access, a valid Groq API key, and service
  availability.
- Future improvements could add configurable log parsers, large-file chunking,
  automated tests, selectable models, and a graphical interface.