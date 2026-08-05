---
name: apple-notes
displayName: Apple Notes
description: 在 macOS 上通过 `memo` CLI 管理 Apple Notes（创建、查看、编辑、删除、搜索、移动和导出备忘录）。当用户请求添加、列出、搜索备忘录或管理文件夹时使用。
version: 1.0.0
tags:
  - knowledge_management
license: Unknown
---

# Apple Notes CLI

Use `memo notes` to manage Apple Notes directly from the terminal. Create, view, edit, delete, search, move notes between folders, and export to HTML/Markdown.

Setup
- Install (Homebrew): `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`
- Manual (pip): `pip install .` (after cloning the repo)
- macOS-only; if prompted, grant Automation access to Notes.app.

View Notes
- List all notes: `memo notes`
- Filter by folder: `memo notes -f "Folder Name"`
- Search notes (fuzzy): `memo notes -s "query"`

Create Notes
- Add a new note: `memo notes -a`
  - Opens an interactive editor to compose the note.
- Quick add with title: `memo notes -a "Note Title"`

Edit Notes
- Edit existing note: `memo notes -e`
  - Interactive selection of note to edit.

Delete Notes
- Delete a note: `memo notes -d`
  - Interactive selection of note to delete.

Move Notes
- Move note to folder: `memo notes -m`
  - Interactive selection of note and destination folder.

Export Notes
- Export to HTML/Markdown: `memo notes -ex`
  - Exports selected note; uses Mistune for markdown processing.

Limitations
- Cannot edit notes containing images or attachments.
- Interactive prompts may require terminal access.

Notes
- macOS-only.
- Requires Apple Notes.app to be accessible.
- For automation, grant permissions in System Settings > Privacy & Security > Automation.
