# hep-paper-writing

A Claude skill for writing experimental and phenomenological high-energy-physics papers in the clear, story-driven style of five papers from Daniel Whiteson's group. The skill itself is `SKILL.md`; `references/` holds the evidence and examples, and `scripts/style_check.py` checks a draft against the measured style.

## Install for Claude Code

```bash
git clone https://github.com/powerofjinbo/hep-writing-skill.git ~/.claude/skills/hep-paper-writing
```

Restart Claude Code. The skill triggers on paper-writing requests, or call it with `/hep-paper-writing`.

To update later:

```bash
git -C ~/.claude/skills/hep-paper-writing pull
```
