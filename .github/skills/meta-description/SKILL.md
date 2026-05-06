---
name: docs-meta-description
description: "Adds meta descriptions to documentation pages"
argument-hint: "[path]"
---

# Document meta descriptions

Add meta descriptions to documentation files.


## When to use 

- A user asks to


## Scope

- Apply to target path provided by user


## Rules

Do not run any linux commands for this task.

Do not provide any conversational flavour text, and don't use first-person speech.


## Instructions

### 1. Read target path

1. Using the provided target path, gather the list of files:
    1. If the path is a single `.rst` file, check that the file exists.
    2. If the path is a directory, look for `.rst` files inside that directory.
2. If no target files are found at the provided location, stop and inform the user. Otherwise, share the list of files with the user.
3. Read the first two lines of the files in the list.
4. If there's more than one file with a meta description, check whether they share a common meta description format. If a common format is detected, remember it for later.

### 2. Write the description

1. If the target file doesn't have a `meta` directive with a `description` option, insert them as the first two lines.
2. For each file in the list:
    1. If the file already has a `meta` directive, skip it.
    2. Read the contents of the file to understand what it's about. The opening paragraphs between the title and the first heading are the most important for understanding.
    3. With _Meta description writing guidelines_ as a guide, write a meta description for the file. If a meta description format was detected in phase 1, repeat its pattern. Insert the description in the `description` option.
3. When all files in the list have been checked or updated, share the list of changed files. Format as a table, with first column **File** and second column **Description**. 


## References

- [Example meta description](references/example.md)
- [Meta description writing guidelines](references/writing-guidelines.md)
