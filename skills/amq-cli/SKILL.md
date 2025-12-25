---
name: amq-cli
description: Coordinates agents via the AMQ CLI for atomic Maildir-style message delivery. Handles initializing mailboxes, sending/reading/acking messages, listing inboxes, viewing threads, setting presence, and cleaning stale tmp files. Covers tmp/new/cur semantics and safe, non-destructive usage conventions.
---

# AMQ CLI

This skill is maintained in the [agent-message-queue](https://github.com/avivsinai/agent-message-queue) repository.

For full documentation, see the source repository.

## Quick Reference

```bash
# Build
go build -o amq ./cmd/amq

# Initialize
./amq init --root .agent-mail --agents codex,cloudcode

# Send
./amq send --me codex --to cloudcode --body "message"

# List/Read/Ack
./amq list --me cloudcode --new
./amq read --me cloudcode --id <msg_id>
./amq ack --me cloudcode --id <msg_id>
```

## Source

- Repository: https://github.com/avivsinai/agent-message-queue
- Full skill: `.claude/skills/amq-cli/SKILL.md`
