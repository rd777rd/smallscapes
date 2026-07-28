# SmallScapes

Marketing site for SmallScapes LLC, an Indiana-based premium hardscaping and landscape construction company. Showcases completed project work and drives direct call/email estimate requests.

**Live site:** https://smallscapes.onrender.com/

## Tech Stack
- Django 4.2, SQLite
- WhiteNoise (static file serving/compression)
- Statically compiled utility CSS (see "Styling" below — no Tailwind CDN/build step required)
- Render (hosting)

## Required environment variables (production)
| Variable | Required | Notes |
|---|---|---|
| `SECRET_KEY` | **Yes** | The app will refuse to start without this when `DEBUG=False`. Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | No (defaults to `False`) | Only set to `True` for local development |
| `ALLOWED_HOSTS` | No (defaults to `smallscapes.onrender.com,localhost,127.0.0.1`) | Comma-separated list; update if the domain changes |
| `DATABASE_URL` | No | Falls back to local SQLite if unset |

## Running locally
```bash
pip install -r requirements.txt
DEBUG=True python manage.py migrate
DEBUG=True python manage.py runserver
```

## Styling
This project ships a statically compiled CSS file (`static/css/compiled-tailwind.css`) generated to cover exactly the utility classes the templates use — there is **no Tailwind CDN `<script>`** and no build step required to deploy. If you add new utility classes to a template, that stylesheet needs to be regenerated/extended to include them, or the new classes won't render.

## Reviews & moderation
Public review submissions go into a pending queue (`is_approved=False`) and are **not** shown on the public Reviews page until a staff user approves them from `/reviews` (while logged in) or the Django admin. This replaced the previous behavior where anyone could publish unmoderated reviews instantly.

## Known open items (not fixed in this pass — need your input)
- **Footer social icons** (Facebook/Instagram/Yelp) still link to `#`. Real profile URLs weren't available — swap them in `templates/partials/_footer.html` once you have them.
- **Project photos**: most before/after images are hosted externally on `i.ibb.co`. Two pairs (`img1`/`img1a`, `img2`/`img2a`) already exist locally in `static/img/` but aren't wired up yet, and the remaining 6 pairs (`img3`–`img8`) aren't in this repo at all — only on ibb.co. To fully self-host: add the missing image files to `static/img/`, optimize them (they're currently 1.1–1.3MB each, uncompressed), and update the `src`/`onclick` URLs in `templates/projects.html` and `templates/home.html` to use `{% static %}` tags instead of the ibb.co links.
