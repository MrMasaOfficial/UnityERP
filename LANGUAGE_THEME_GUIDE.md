# Language and Theme Guide

## Overview

Full language and theme support (Dark/Light Mode) has been added to the app:

- **Supported Languages**: Arabic (AR) and English (EN)

- **Supported Themes**: Day Mode (Light) and Night Mode (Dark)
- **Save Settings**: User preferences are saved automatically

## Using the App

### 1. First Launch

When you launch the app for the first time:

- Default Language: **Arabic**

- Default Theme: **Day Mode (Light)**

### 2. Accessing Settings

1. In the main window, go to the **Settings** menu at the top.

2. Select **Settings** from the drop-down menu.

3. The settings window will appear.

### 3. Changing the Language

In the settings window:

1. Select the desired language from the **Language** list:

- **Arabic**

- **English**

2. Tap **Save**

3. The app will update Automatically configure the app interface

### 4. Change the appearance

In the settings window:

1. Select the desired theme from the **Theme** list:

- **Light Mode** (Daytime Mode)

- **Dark Mode** (Night Mode)

2. Click **Save**

3. The new theme will be applied immediately

### 5. Save settings

- All settings are automatically saved in the `app_settings.json` file.
- Your settings will be saved when you close and restart the app.

## Main files

### `translations.py`
Contains all text in Arabic and English

**Usage**:

```python
from translations import t

label = QLabel(t('name')) # Displays "Name" in Arabic or "Name" in English

```

### `themes.py`
Manages themes and colors

**Usage**:

```python
from themes import get_stylesheet, set_theme

set_theme('dark')
app.setStyleSheet(get_stylesheet())

```

### `settings.py`
Manages saving and restoring settings

**Usage**:

```python
from settings import settings_manager

lang = settings_manager.get_language() # 'ar' or 'en'
settings_manager.set_language('en')

```

## Settings file (`app_settings.json`)

Settings are saved in this file:

```json
{
"language": "ar",

"theme": "light",

"window_geometry": null,

"window_state": null
}

```

## Main translated keys

| Key | Arabic | English |

|---------|---------|-----------|

| title | Integrated ERP System |

| inventory | Inventory |

| sales | Sales |

| add | Add |

| edit | Edit |

| delete | Delete |

| save | Save |

| success | Success |

| error | Error |

## Colors and Styles

### Light Mode
- Background: White (#ffffff)
- Text: Black (#000000)
- Buttons: Dark Blue (#1f4788)

### Dark Mode
- Background: Very Dark Gray (#1e1e1e)
- Text: Light Gray (#e0e0e0)
- Buttons: Medium Blue (#2a5fa0)

## Adding New Languages

To add a new language (e.g., French):

1. Open the `translations.py` file

2. Add a new language to the `TRANSLATIONS` dictionary:

```python
TRANSLATIONS = {
'ar': { ... },

'en': { ... },

'fr': { # Add French
'title': 'Système ERP intégré',

'inventory': 'Inventaire',

# ... etc.

}
}
```

3. Add the option in the settings window (in `main.py`)

## Tips and Notes

1. **Merged Scripts**: Use `t()` for all text displayed to the user.

2. **Performance**: The system is optimized and does not affect performance.

3. **Compatibility**: Works with all Windows, Linux, and macOS platforms.

4. **Customization**: Colors and styles can be modified in the `themes.py` file.

## Suggested Next Steps

- Update all other UI files (sales, purchasing, accounting, reports)
- Add additional languages
- Add more custom themes
- Full RTL (Right-to-Left) support for Arabic
