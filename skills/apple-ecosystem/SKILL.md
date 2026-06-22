---
name: apple-ecosystem
description: "Apple platform integrations: notes, reminders, messages, Find My, and computer automation on macOS/iOS."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [apple, macos, ios, notes, reminders, findmy, imessage, automation, computer-use]
---

# Apple Ecosystem Integration

Unified entry point for Apple platform skills. Load the subsection that matches
the requested service or workflow.

## Notes: apple-notes

Read, create, and edit Apple Notes on macOS/iOS via native tooling.

**Triggers:** Apple Notes, iCloud notes, note-taking on iPhone/Mac.

See standalone `apple-notes` for setup, commands, and platform constraints.

## Reminders: apple-reminders

Manage Apple Reminders lists, tasks, due dates, and priorities.

**Triggers:** Apple Reminders, to-do lists, task management on iPhone/Mac.

See standalone `apple-reminders` for setup, commands, and platform constraints.

## Find My: findmy

Locate Apple devices and share location via the Find My network.

**Triggers:** Find My, locate iPhone, share location, device location.

See standalone `findmy` for setup, commands, and platform constraints.

## Messages: imessage

Send and receive iMessages from the agent on macOS.

**Triggers:** iMessage, text someone on Messages, send SMS/MMS from Mac.

See standalone `imessage` for setup, commands, and platform constraints.

## macOS Computer Use: macos-computer-use

Control a macOS desktop (clicks, typing, screenshots) for automation.

**Triggers:** control my Mac, click this button on macOS, automate macOS.

See standalone `macos-computer-use` for setup, permissions, and automation patterns.

## Platform Support

Most Apple skills require **macOS** and are unsupported on Windows/Linux.
If the host is non-macOS, surface that limitation before attempting setup.
