To include in pydantic models:
```
NOTE:
  - use a tuple where both helpful: (id, name)
  - id without an example means int
  - name without an example means str
```
- user
  - user id
  - full name
  - title name: 'Site Director'
  - clearance lvl: (1, 'Level 1 - Unrestricted')
  - assigned site id


- scp
  - scp id
  - classification lvl: (1, 'Level 1 - Unrestricted')
  - containment class: (1, 'Safe')
  - secondary class: (1, 'Thaumiel')
  - risk class: (1, 'Level 1 - Notice')
  - disruption class: (1, 'Level 1 - Dark')
  - site responsible id
  - assigned task force name
  - status: ('active', 'neutralized', 'explained', 'deleted')
  - created_at: sql datetime
  - updated_at: sql datetime

- scp_colours: #XXXXXX
  - classification lvl
  - containment class
  - secondary class
  - risk class
  - disruption class


- site
  - site name
  - site id
  - director: (1, 'John Doe')
  - site location: str


- mtf
  - mtf name
  - mtf nickname
  - mtf id
  - assigned site id
  - leader: (1, 'John Doe')
  - active: bool


- redacted
  - file_classification: 'Level 1 - Unrestricted', etc.
  - usr_clearance: 'Level 1 - Unrestricted', etc.
- clearance_denied
  - needed_clearance: 'Level 1 - Unrestricted', etc.
  - usr_clearance: you get it


# Display Module TODO List

## helpers.py - TODOs

### High Priority
- [ ] **Add input validation to `printc()`**
  - Validate [`string`]helpers.py ) is actually a string
  - Handle empty strings gracefully

- [ ] **Add docstring parameters documentation**
  - Document [`end`]helpers.py ) and [`flush`]helpers.py ) parameters in [`printc()`]helpers.py )
  - Add parameter types to all docstrings

### Medium Priority
- [ ] **Add error handling to `clear()`**
  - Wrap [`system()`](/c:/Users/packa/AppData/Local/Programs/Python/Python313/Lib/os.py ) calls in try-except
  - Handle cases where shell commands fail

- [ ] **Consider timezone awareness in `timestamp()`**
  - Add optional timezone parameter
  - Document that current implementation uses local time

### Low Priority
- [ ] **Add `__all__` export control**
  - Explicitly define what functions are public API

---

## config.py - TODOs

### High Priority
- [ ] **Fix `MAX_BOX_SIZE` validation**
  - Currently defined but never enforced
  - Add validation in [`basic_box()`](CS50xFP/utils/display/core/boxes.py ) that uses this constant

### Medium Priority
- [ ] **Document why `MIN_TERM_WIDTH = 120`**
  - Add comment explaining this specific width requirement
  - Consider if this could be configurable

- [ ] **Add validation for color codes**
  - Validate hex codes in [`CLEAR_LVL_COLOURS`]config.py ) are valid
  - Consider using a color validation function

### Low Priority
- [ ] **Consider environment variable overrides**
  - Allow [`MIN_TERM_WIDTH`]config.py ) to be set via environment variable
  - Useful for testing or special deployments

---

## system.py - TODOs

### High Priority
- [ ] **Extract magic numbers from `sim_load()`**
  ```python
  sleep(expovariate(2))  # What does 2 represent?
  if choice([True, False, False, False]):  # 25% chance
  ```
  - Create constants: [`LOAD_RATE = 2`]system.py ), [`HICCUP_PROBABILITY = 0.25`]system.py )

- [ ] **Fix code duplication in `login()`**
  - Three very similar blocks for O5/Director/Administrator
  - Extract common pattern into helper function

### Medium Priority
- [ ] **Add user validation in `login()`**
  - Validate [`usr`]system.py ) is not None
  - Validate required fields exist

- [ ] **Make ASCII art configurable**
  - Consider loading from external file
  - Allows customization without code changes

### Low Priority
- [ ] **Consider async for `sim_load()`**
  - Current blocking could be improved with async/await
  - Low priority since it's intentionally blocking for effect

---

## access.py - TODOs

### High Priority
- [ ] **Standardize parameter naming**
  ```python
  def redacted(file: str, file_classification: str, usr_clearance: str)
  def expunged(file: str)
  def granted(file: str)
  ```
  - [`file`]access.py ) should be [`file_ref`]access.py ) for consistency with displayed text
  - Or rename displayed text to match parameter

- [ ] **Add input validation**
  - Validate all parameters are strings and non-empty
  - Add type checking

### Medium Priority
- [ ] **Add comprehensive docstrings**
  - Document all parameters
  - Add examples of usage
  - Document the RAISA logging behavior

### Low Priority
- [ ] **Consider extracting message templates**
  - Move fixed strings to configuration
  - Allows localization in future

---

## create.py - TODOs

### High Priority
- [ ] **Missing import: `f_id` function**
  ```python
  from .helpers import f_id as format_id
  ```
  - This function doesn't exist in helpers.py!
  - Either create it or use inline formatting

- [ ] **Add input validation to all functions**
  - Validate string parameters are non-empty
  - Validate [`f_id`]create.py ) is positive integer

### Medium Priority
- [ ] **Extract repeated constants**
  ```python
  PERSISTS = 'CONTACT YOUR SITE...'
  TRY_AGAIN = [...]
  ```
  - Good start, but more can be extracted
  - Consider moving to configuration

- [ ] **Standardize function naming**
  - [`create_f`]create.py ), [`invalid_f_type`]create.py ), [`invalid_f_data`]create.py ), [`created_f`]create.py )
  - Use full word "file" for consistency

### Low Priority
- [ ] **Add comprehensive docstrings**
  - Document parameters and their formats
  - Add usage examples

---

## art.py - TODOs ⚠️ **Needs Major Refactoring**

### Critical Priority
- [ ] **Missing imports - Code won't run!**
  ```python
  from .helpers import *  # What's imported?
  ```
  - [`COLOURS`]art.py ) is undefined (should be [`CLEAR_LVL_COLOURS`]config.py ))
  - Functions like [`acs_bar()`](CS50xFP/utils/display/core/bars/bars.py ), [`site_bar()`](CS50xFP/utils/display/core/bars/bars.py ), [`mtf_bar()`](CS50xFP/utils/display/core/bars/bars.py ), [`user_bar()`](CS50xFP/utils/display/core/bars/bars.py ) not imported
  - [`print_table_users()`](CS50xFP/utils/display/core/tables.py ) not imported
  - Fix all imports explicitly

### High Priority
- [ ] **Code duplication in interactive loops**
  ```python
  # display_scp, display_site, display_mtf all have similar patterns
  while True:
      print()
      if keys:
          for i, key in enumerate(keys):
              print(f'{i}: {key}')
      print('C: close file')
      # ... handling logic
  ```
  - Extract to `_display_additional_files()` helper function

- [ ] **Inconsistent error handling**
  ```python
  except ValueError or IndexError:  # Wrong! This is always True
  ```
  - Should be: `except (ValueError, IndexError):`
  - Fix in both [`display_scp()`]art.py ) and [`display_site()`]art.py )

- [ ] **Add input validation**
  - Validate all [`Models.*`](CS50xFP/utils/sql/models.py ) parameters are not None
  - Validate required fields exist
  - Handle missing relationships gracefully

### Medium Priority
- [ ] **Simplify `display_scp()` addenda handling**
  ```python
  if addenda:
      a_names: list[str] = [key for key in addenda.keys()]
  else:
      a_names = []
  ```
  - Simplify: `a_names = list(addenda.keys()) if addenda else []`

- [ ] **Remove unnecessary variable decrement**
  ```python
  i -= 1  # After removing from a_names
  ```
  - This does nothing useful, remove it

- [ ] **Add comprehensive docstrings**
  - Document all parameters
  - Explain the interactive loop behavior
  - Document keyboard commands

### Low Priority
- [ ] **Consider extracting keyboard commands to config**
  ```python
  print('C: close file')
  if inp.upper() == 'C':
  ```
  - Make commands configurable
  - Add help command listing all options

---

## Critical Issues Summary 🚨

### **Must Fix Before Running:**

1. **art.py import errors** - Code will crash immediately
   - Import [`CLEAR_LVL_COLOURS`]config.py ) as COLOURS
   - Import all bar functions from [`core.bars`](CS50xFP/utils/display/core/bars/bars.py )
   - Import [`print_table_users`](CS50xFP/utils/display/core/tables.py ) from [`core.tables`](CS50xFP/utils/display/core/tables.py )

2. **create.py missing function** - [`format_id`]create.py ) doesn't exist
   - Either create it in helpers.py or use inline: `f'{f_id:03d}'`

3. **Exception handling bug** - Will catch wrong exceptions
   - Fix: `except (ValueError, IndexError):` not `except ValueError or IndexError:`

---

## Refactoring Recommendations

### Extract Common Interactive Pattern
```python
# New helper in helpers.py or art.py
def display_additional_content(
    items: dict[str, str],
    console: Console,
    prompt: str = 'Display additional files?'
) -> None:
    """Generic handler for showing additional content with interactive menu"""
    available_keys = list(items.keys())

    while available_keys:
        print()
        print(prompt)

        for i, key in enumerate(available_keys):
            print(f'{i}: {unquote(key)}')
        print('C: close')

        choice = input('> ')

        if choice.upper() == 'C':
            return

        try:
            idx = int(choice)
            key = available_keys[idx]
            console.print(Md(f'## {unquote(key)}\n\n{items[key]}'))
            available_keys.remove(key)
        except (ValueError, IndexError):
            print(f'INVALID CHOICE: {choice!r}')
```

### Simplify `login()` Function
```python
# Create a data structure for login messages
LOGIN_MESSAGES = {
    'O5 Council Member': {
        'title': '<< O5 AUTHORIZATION VERIFIED >>',
        'clearance': 'CLEARANCE LEVEL: 6 - COSMIC TOP SECRET',
        'welcome': 'Welcome back, {name}.',
        'logging': 'This session is being logged by CoreNode Zero.',
        'status': 'SYSTEM STATUS: OPERATIONAL | DEEPWELL CHANNEL ENCRYPTED'
    },
    # ... similar for other titles
}

def _format_login_line(text: str, width: int = 112) -> str:
    """Helper to format login message lines"""
    return '////' + f'{text:^{width}}' + '////'

def login(usr: Models.User) -> None:
    messages = LOGIN_MESSAGES.get(usr.title.name)

    if messages:
        # Build formatted message from template
        # ... much cleaner implementation
    else:
        # Default simple message
```

---

## Priority Order - Overall

### 🔴 **Critical (Fix Immediately)**
1. Fix imports in art.py
2. Fix/create [`format_id()`]create.py ) in create.py
3. Fix exception handling syntax in art.py

### 🟡 **High Priority (Before Production)**
4. Add input validation across all display functions
5. Extract common interactive loop pattern
6. Refactor [`login()`]system.py ) to eliminate duplication
7. Fix magic numbers in [`sim_load()`]system.py )

### 🟢 **Medium Priority (Quality Improvements)**
8. Add comprehensive docstrings
9. Standardize naming conventions
10. Extract more constants to configuration
11. Add error handling to [`clear()`]helpers.py )

### 🔵 **Low Priority (Future Enhancements)**
12. Consider async for loading animations
13. Add localization support
14. Make ASCII art configurable

---

## Estimated Impact

- **Critical fixes**: ~30 minutes, code won't run without these
- **High priority**: ~2-3 hours, significantly improves code quality
- **Medium priority**: ~2-4 hours, professional polish
- **Low priority**: Future work, nice-to-have features
