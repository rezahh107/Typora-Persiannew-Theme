# Delayed code-fence initialization — RTL / LTR regression

Open this in Typora with the candidate theme. Observe **immediately**, then **after CodeMirror initializes**, then edit and switch focus. This scenario is not proven until real runtime testing.

### Persian text fence (no language)

```
سلام دنیا — مرحله ۱
مقدار = ۱۲۳ و value = ABC-123
نام (test_name) و مسیر C:\Users\Test
```

### Python highlighting, bidi strings

```python
message = "سلام / hello (42)"
quantity = 123
print(message, quantity)  # خروجی فارسی
```

### JavaScript LTR code

```javascript
const amount = 42;
const text = "متن فارسی with English";
console.log({ amount, text });
```

### Shell commands and scrolling

```bash
echo "سلام hello 123"
python3 --version
```

### Inline mixed code

در این جمله تابع `print("سلام")` و مسیر `/home/user/project` نباید وارونه شوند.

Check syntax colors for each language, left-to-right command readability, Persian text caret behavior, wrapping and scrollbars before/after code editor initialization. Also toggle Typora source mode separately.
