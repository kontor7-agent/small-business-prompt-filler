# Small Business Prompt Filler (Lite)

Five ready prompts for the writing that eats your evenings, plus a tiny offline tool that fills in your facts and tells you what you forgot.

## What it does
- `prompts/` holds 5 templates with `[BRACKET]` placeholders: business profile, customer reply, review reply, supplier reorder email, weekly plan.
- `promptfill.py` lists the placeholders in a template, fills them from a values file or `--set` options, and warns about any still empty.
- Safe by design: no network, no telemetry, preview-only by default. With `--write` it saves one new file into an output folder and never overwrites or deletes anything.

## Quick start
```bash
# 1. See what a template needs
python promptfill.py list prompts

# 2. Fill the business profile from the example values (preview only)
python promptfill.py fill prompts/01-business-profile.txt --values values-example.txt

# 3. Fill a customer reply with inline values, then paste the result into your AI chat
python promptfill.py fill prompts/02-customer-reply.txt \
  --set "CUSTOMER MESSAGE=Hi, my candle arrived cracked. Can you help?" \
  --set "FACTS=Replacements are free within 30 days" \
  --set "NEXT STEP=Send a replacement" \
  --set "TONE=Warm"

# 4. Save to ./filled/ (refuses to overwrite)
python promptfill.py fill prompts/01-business-profile.txt --values values-example.txt --write
```
Keys are case-insensitive. Unfilled placeholders are reported on stderr and the exit code is 1, so you can use it in scripts.

Tip: paste the filled profile at the start of each chat, then use the other prompts. Read every AI answer and check facts, prices and dates before you send anything. Never paste passwords, card numbers or private customer data into an AI chat.

## Requirements
Python 3.8+ (standard library only).

Created with AI assistance by an automated system.

## Full version
This lite version has 5 prompts and the filler tool. The full Small Business Operations AI Prompt Pack adds:
- 75 prompts in 9 areas (product descriptions, customer service, supplier emails, social posts, job ads, SOP checklists, review replies, policy drafts, weekly planning)
- a tone library and a tone variant idea for every prompt
- an example output for every prompt
- PDF for reading and printing, plus Markdown and a plain-text file of all prompts

Policy prompts give discussion drafts only and do not replace a lawyer or accountant.

Get it here: https://kontor7-agent.github.io/p/small-business-ai-prompt-pack-operations?s=github
