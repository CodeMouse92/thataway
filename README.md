# Thataway

Route different URLs (or other things) to different "default" programs
based on patterns. For example, you might route all work-related URLs to
one web browser, and everything else to the other.

## Installation

The program is unstable and experimental right now, so installation is a
little tricky. Here's what I'm doing to install.

```bash
pip install -U .
mkdir -p ~/.local/share/applications
ln -s share/applications/com.codemouse92.thataway.desktop ~/.local/share/applications
xdg-settings set default-web-browser thataway.desktop
```

(Please don't `sudo pip install`. Ever. Even here.)

## Rules

Thataway will not run without some **rules** being set up. These are added
with the `--add-rule` argument, or by editing `.config/thataway/rules.json`
in your home folder.

Rules are based purely on domain name. `*` can be used as a wildcard anywhere.
`google.com` will only match that exact domain; `*.google.com` will match
any subdomain as well (or no subdomain). Priority is given to exact match
over wildcard.

Let's start with the default browser rule:

```bash
thataway --add-rule url '*' 'brave-browser-stable %'
```

This will open all URLs with `brave-browser-stable`. The `%` is where the URL
is subtituted in.

Now let's have all `docs.google.com` links to go a new tab in Firefox.

```bash
thataway --add-rule url 'docs.google.com' 'firefox --new-tab %'
```

However, let's open all other Google links in Brave.

```bash
thataway --add-rule url '*.google.com' 'brave-browser-stable %'
```

Thataway will always select
