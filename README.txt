Building and publishing Python wheels using **`uv`** is straightforward. Because this is a pure-Python project that depends on `numpy`, **`uv` can act as both your project manager and build frontend/backend**.

You **do not need any extra tools** (like `setuptools`, `flit`, or `twine`) unless you want to write native C or Rust code extensions for NumPy (in which case you would use tools like `scikit-build-core` or `maturin`). For a pure Python library, `uv` has everything built-in.

Here is the complete step-by-step guide from setting up your empty Git repo to publishing your wheel.

---

### Step 1: Clone Your Empty GitHub Repo Locally

First, pull down your empty repository:

```bash
git clone git@github.com:deanagan/test-wheels.git
cd test-wheels

```

---

### Step 2: Initialize a Python Library Project with `uv`

Run `uv init` with the `--lib` flag inside your repo:

```bash
uv init --lib

```

This sets up a standard Python library template with a `src/` layout:

* `pyproject.toml` (Project configuration, dependencies, and build settings)
* `src/test_wheels/` (Where your code lives)
* `src/test_wheels/__init__.py`
* `.python-version` & `.gitignore`

---

### Step 3: Add `numpy` as a Dependency

Tell `uv` to add `numpy` to your library's `dependencies` table in `pyproject.toml`:

```bash
uv add numpy

```

---

### Step 4: Write the Calculator Code

Open `src/test_wheels/calculator.py` and write your basic NumPy calculator logic:

```python
import numpy as np

class Calculator:
    """A basic calculator using NumPy arrays."""

    @staticmethod
    def add(a: list[float], b: list[float]) -> list[float]:
        """Element-wise addition of two lists."""
        arr_a = np.array(a)
        arr_b = np.array(b)
        return (arr_a + arr_b).tolist()

    @staticmethod
    def multiply(a: list[float], b: list[float]) -> list[float]:
        """Element-wise multiplication of two lists."""
        arr_a = np.array(a)
        arr_b = np.array(b)
        return (arr_a * arr_b).tolist()

    @staticmethod
    def mean(numbers: list[float]) -> float:
        """Calculates the mean of a list of numbers."""
        return float(np.mean(numbers))

```

Next, expose your `Calculator` class in `src/test_wheels/__init__.py`:

```python
from test_wheels.calculator import Calculator

__all__ = ["Calculator"]

```

---

### Step 5: Test Your Code Locally

You can quickly run Python in `uv`'s environment to test your code:

```bash
uv run python -c "from test_wheels import Calculator; print(Calculator.add([1, 2], [3, 4]))"

```

*Output should be: `[4.0, 6.0]*`

---

### Step 6: Build Your Wheel (`.whl`) and Source Archive (`.tar.gz`)

To build the distribution packages, simply run:

```bash
uv build

```

`uv` will build two files into a new `dist/` directory:

1. **Source Distribution (`sdist`)**: `dist/test_wheels-0.1.0.tar.gz`
2. **Wheel (`bdist_wheel`)**: `dist/test_wheels-0.1.0-py3-none-any.whl`

*(The `.whl` file is a pre-compiled Python distribution containing your source code and specifying `numpy` as a required install dependency).*

---

### Step 7: Push Your Source Code to GitHub

Save your code changes to Git:

```bash
git add .
git commit -m "feat: setup library and add numpy calculator"
git push -u origin main

```

---

### Step 8: Upload Your Wheel to PyPI (or TestPyPI)

#### Option A: Publish to **TestPyPI** (Recommended for Learning)

Before uploading to the real PyPI, test the publishing process on [TestPyPI](https://testpypi.org/?utm_source=gemini):

1. Create a free account on [TestPyPI](https://www.google.com/search?q=https://testpypi.org/account/register/&utm_source=gemini).
2. Go to **Account Settings** -> **API tokens** and generate a new token.
3. Publish using `uv publish`:

```bash
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-YOUR_TEST_PYPI_TOKEN

```

4. **Verify Installation:** Test installing your uploaded wheel in a clean `uv` environment:
```bash
uv run --isolated --extra-index-url https://test.pypi.org/simple/ --with test-wheels python -c "from test_wheels import Calculator; print(Calculator.mean([10, 20, 30]))"

```



---

#### Option B: Publish to Real **PyPI**

When you are ready to publish for the public:

1. Create an account on [PyPI.org](https://pypi.org/?utm_source=gemini).
2. Generate an API Token under **Account Settings**.
3. Upload your built package:

```bash
uv publish --token pypi-YOUR_PYPI_TOKEN

```

Once uploaded, anyone anywhere can install your package via `pip install test-wheels` or `uv add test-wheels`!