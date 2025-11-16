# Quick Start - ERP System

## Installation and Startup

### 1. Installation

```bash
# Install Libraries
pip install -r requirements.txt

# Add Initial Data (Optional)
python seed_data.py

```

### 2. Run the Application

```bash
python main.py

```

## Using New Features

### Switching Language Between Arabic and English

1. Tap the **Settings** menu at the top

2. Select **Settings**

3. Choose Language from the **Language** menu

4. Tap **Save**

**Result**: All text and menus will be updated automatically

### Switching Theme (Dark/Light)

1. Tap the **Settings** menu at the top

2. Select **Settings**

3. Choose Theme from the **Theme** menu:

- **Light Mode**: Daytime Mode

- **Dark Mode**: Dark Mode Night Mode
4. Press **Save**

**Result**: The new colors will be applied to everything

## Available Features

| Feature | Status | Description |

|-------|--------|--------|

| **Multilingual Mode** | ✅ Ready | Arabic & English |

| **Dark Mode** | ✅ Ready | Full Night Mode |

| **Light Mode** | ✅ Ready | Classic Day Mode |

| **Save Settings** | ✅ Ready | Automatically Saves |

| **GUI** | ✅ Ready | Simple & Beautiful |

| **Database** | ✅ Ready | Optimized SQLite |

## Main Interfaces

1. **Inventory**

- Item Management

- Inventory Transactions

- Quantity Alerts

2. **Sales**

- Invoice Creation

- Customer Management

- Invoice Printing

3. **Purchasing**

- Purchase Orders

- Supplier Management

- Receiving Purchases

4. **Accounting**

- Account Management

- Financial Transactions

- Customer and Supplier Accounts Receivable

5. **Reports**

- Sales Reports

- Purchase Reports

- Financial Reports

## Useful Shortcuts

### To Refresh Data

Press the **Refresh** button in any interface

### To Add a New Item

Press **Add** or **New**

### To Delete an Item

Select the item and press **Delete**

### To Print a PDF

Select the item and press **Print PDF**

## Troubleshooting Common Issues

### Issue: No Text Displays Correctly

**Solution**:
1. Ensure the correct libraries are installed.
2. Restart the application.
3. Change the language in Settings and then re-enable it.

### Problem: Dark Mode Not Applied to the Full Setting

**Solution**:
1. Go to Settings.
2. Ensure Dark Mode is selected.
3. Tap Save.
4. Restart the application.

### Problem: Raw Data Not Added

**Solution**:
```bash
python seed_data.py
```

## File Structure

```
erp_system/
├── main.py # Main Program
├── database.py # Database
├── translations.py # Languages
├── themes.py # Themes
├── settings.py # Settings
├── ui/ # Interfaces
├── utils/ # Tools
├── app_settings.json # User Settings
└── erp_system.db # Database

## Translated Keys

Over 60 comprehensive translation keys are available:
- Names (items, customers, suppliers, etc.)
- Actions (add, edit, delete, save, etc.)
- Messages (success, error, warning, etc.)
- Fields (name, price, quantity, date, etc.)

## Future Development

We can easily:
- ✅ Add new languages
- ✅ Customize colors and themes
- ✅ Add customer-specific adaptations
- ✅ Improve performance
- ✅ Add new features

## Support and Help

For more information:
- Read `LANGUAGE_THEME_GUIDE.md` for full details
- Read `UPDATES.md` for the latest updates
- Read `README.md` for general information

## License

This project is open source and free to use.

---

**Version 1.0** - With language and theme support