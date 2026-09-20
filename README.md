<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img alt="jules-bot" src="assets/logo-light.svg" width="540">
  </picture>
</p>

<p align="center">
  <img alt="python" src="https://img.shields.io/badge/python-3.11-2BD9FF">
  <img alt="docker" src="https://img.shields.io/badge/docker-ready-2BD9FF">
  <img alt="access" src="https://img.shields.io/badge/access-single%20user-2BD9FF">
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-MIT-2BD9FF"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#using-it">Using it</a> ·
  <a href="#configuration">Configuration</a> ·
  <a href="#authentication">Auth</a> ·
  <a href="#deploying">Deploying</a>
</p>

**Start a [Google Jules](https://jules.google.com) coding session from your phone.**

Text the bot what you want done, tap the repo from the buttons it replies with, and it hands back
the Jules session link. That's the whole loop.

The reason it exists: Jules runs asynchronously and does the work on its own. The only part that
genuinely needs you at a keyboard is *typing the task*. This removes that requirement, so a job
can start from a parking lot or a lecture hall and be waiting for you when you get back.

## Quick start

```bash
docker build -t jules-bot .
docker run \
  -e BOT_TOKEN=... \
  -e TELEGRAM_USER_ID=... \
  -e JULES_REPOS=site:lukejacobsen7/current-layer-site,scanner:lukejacobsen7/Options_Chain \
  jules-bot
```

The image ships with the Jules CLI already installed.

## Using it

| You send | It does |
| --- | --- |
| Any message | Replies with one button per configured repo, then fires Jules at the one you pick and returns the session link |
| `/auth` | Runs the Jules CLI login and forwards the device code to you, so you can authenticate with no shell access |

## Configuration

| Variable | Meaning |
| --- | --- |
| `BOT_TOKEN` | Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_USER_ID` | Your numeric Telegram user ID — the only sender allowed to talk to it |
| `JULES_REPOS` | Repo list as `label:owner/repo`, comma separated |
| `PORT` | Health-check port (default `8080`) |

Example:

```
JULES_REPOS=site:lukejacobsen7/current-layer-site,scanner:lukejacobsen7/Options_Chain
```

## Access control

Only `TELEGRAM_USER_ID` is allowed to talk to it. **Every other sender is ignored silently** — no
reply, no error, no hint that the bot exists. A Telegram bot username is guessable, so an
allowlist is the only thing between a stranger and your repos.

## Authentication

Jules authenticates by device code. `/auth` starts that flow inside the container and forwards the
code to your chat, so you can complete the login from your phone without SSH-ing anywhere.

## Deploying

There is a plain HTTP health endpoint on `PORT`, so it runs on any platform that requires one —
Cloud Run, Railway, Fly, Render.

## License

MIT — see [LICENSE](LICENSE).
