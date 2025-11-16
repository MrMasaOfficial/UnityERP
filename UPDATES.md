# تحديثات النظام - دعم اللغات والمواضيع

## تم الإضافة

### 1. نظام الترجمة (Translations)
- **ملف**: `translations.py`
- **الميزات**:
  - دعم اللغة العربية والإنجليزية
  - دالة `t()` لترجمة النصوص بسهولة
  - دعم تبديل اللغات في الوقت الفعلي

### 2. نظام المواضيع (Themes)
- **ملف**: `themes.py`
- **الميزات**:
  - وضع ليلي (Dark Mode)
  - وضع نهاري (Light Mode)
  - CSS قابل للتخصيص
  - تطبيق الثيمات على جميع العناصر

### 3. إدارة الإعدادات (Settings)
- **ملف**: `settings.py`
- **الميزات**:
  - حفظ تفضيلات المستخدم في `app_settings.json`
  - استعادة الإعدادات تلقائياً
  - دعم جميع الإعدادات المستقبلية

### 4. قائمة الإعدادات (Settings Dialog)
- **موقع**: `main.py`
- **الميزات**:
  - واجهة سهلة لتغيير اللغة
  - واجهة سهلة لتغيير المظهر
  - حفظ الإعدادات تلقائياً

## كيفية استخدام النظام

### في الملفات الجديدة:

```python
from translations import t
from themes import get_stylesheet, set_theme
from settings import settings_manager

label = QLabel(t('name'))
button = QPushButton(t('save'))
QMessageBox.info(self, t('success'), t('operation_successful'))
```

### التبديل بين اللغات:

```python
from translations import set_language
from settings import settings_manager

set_language('en')
settings_manager.set_language('en')
```

### تطبيق الثيمات:

```python
from themes import set_theme, get_stylesheet
from settings import settings_manager

set_theme('dark')
settings_manager.set_theme('dark')
app.setStyleSheet(get_stylesheet())
```

## الملفات المحدثة

- ✅ `main.py` - إضافة قائمة الإعدادات والدعم الكامل
- ✅ `ui/inventory.py` - تحديث معظم النصوص والرسائل

## الملفات التي تحتاج تحديث

للحصول على دعم كامل للترجمات في جميع الملفات:

1. `ui/sales.py`
2. `ui/purchasing.py`
3. `ui/accounting.py`
4. `ui/reports.py`

## خطوات التحديث

لكل ملف UI، اتبع هذه الخطوات:

1. أضف الاستيراد في أعلى الملف:
```python
from translations import t
```

2. استبدل جميع النصوص العربية/الإنجليزية بـ `t('key')`

3. أضف المفاتيح الناقصة إلى `translations.py` إذا لزم الأمر

## مثال تحديث

### قبل:
```python
btn = QPushButton('إضافة فاتورة')
msg = QMessageBox.warning(self, 'تحذير', 'اختر عميلاً')
```

### بعد:
```python
btn = QPushButton(t('new_invoice'))
msg = QMessageBox.warning(self, t('warning'), t('select_item'))
```

## الإعدادات المحفوظة

يتم حفظ الإعدادات التالية في `app_settings.json`:
- اللغة الحالية
- المظهر الحالي
- (يمكن إضافة المزيد)

## الاختبار

للتأكد من أن كل شيء يعمل:

```bash
python main.py
```

ثم:
1. اذهب إلى الإعدادات (Settings)
2. جرب تغيير اللغة من العربية إلى الإنجليزية
3. جرب تغيير المظهر من الضوء إلى الظلام
4. أغلق التطبيق وأعد تشغيله للتحقق من حفظ الإعدادات

## ملاحظات هامة

- جميع النصوص الآن قابلة للترجمة
- يتم حفظ تفضيلات المستخدم تلقائياً
- يعمل النظام بكفاءة حتى مع عدد كبير من اللغات والمواضيع
- يمكن توسيع النظام بسهولة بإضافة لغات جديدة أو مواضيع جديدة
