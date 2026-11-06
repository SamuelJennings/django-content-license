# Internationalization (i18n) for Django Content License

This directory contains translation files for the django-content-license package.

## Available Translations

Currently, the package includes the following languages:

- **English (en)** - Default language
- **Spanish (es)** - Example translation structure

## Adding New Translations

Run every `makemessages` and `compilemessages` command from inside the `licensing/` directory so only the package source is scanned. The `example/` app carries no translation markup and is never translated.

To add a new language translation:

1. **Create locale directory structure:**
   ```bash
   (cd licensing && django-admin makemessages -l <language_code>)
   ```

   For example, for French:
   ```bash
   (cd licensing && django-admin makemessages -l fr)
   ```

2. **Translate the messages:**
   Edit the generated `.po` file in `locale/<language_code>/LC_MESSAGES/django.po`

3. **Compile translations:**
   ```bash
   (cd licensing && django-admin compilemessages)
   ```

## Updating Existing Translations

To update translations when new translatable strings are added:

```bash
(cd licensing && django-admin makemessages --all)
```

Then update the `.po` files and compile:

```bash
(cd licensing && django-admin compilemessages)
```

## Key Translatable Strings

The package includes translations for:

- Model field labels and help text
- Admin interface elements
- License attribution templates
- Status messages ("Active", "Deprecated", "No description", etc.)

## Template Translation

The attribution template uses Django's `{% blocktrans %}` tag with proper fallbacks for different object configurations (with/without creators, URLs, etc.).
