# Jules Bot

A Telegram bot that lets you start [Google Jules](https://jules.google.com)
coding sessions from your phone. Text it what you want done, pick the repo from
the buttons it replies with, and it hands back the session link.

The reason it exists: Jules runs asynchronously and does the work on its own,
so the only part that actually needs you at a keyboard is typing the task. This
removes that requirement.

## Using it

- Send any message — it replies with a button per configured repo, then fires
  Jules at the one you pick.
- `/auth` — runs the Jules CLI login and forwards the device code back to you,
  so you can authenticate without shell access.

Only the Telegram user ID in `TELEGRAM_USER_ID` is allowed to talk to it. Every
other sender is ignored.

## Configuration

| Variable | Meaning |
| --- | --- |
| `BOT_TOKEN` | Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_USER_ID` | Your numeric Telegram user ID — the only allowed sender |
| `JULES_REPOS` | Repo list as `label:owner/repo`, comma separated |
| `PORT` | Health-check port (default `8080`) |

Example:

```
JULES_REPOS=site:lukejacobsen7/current-layer-site,scanner:lukejacobsen7/Options_Chain
```

## Running it

```bash
docker build -t jules-bot .
docker run -e BOT_TOKEN=... -e TELEGRAM_USER_ID=... -e JULES_REPOS=... jules-bot
```

The image includes the Jules CLI. There is a plain HTTP health endpoint on
`PORT` so it can run on a platform that requires one (Cloud Run, Railway, Fly).
