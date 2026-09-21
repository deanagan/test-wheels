Here is the complete, updated step-by-step guide incorporating `uv build --no-sources`, package options (`sdist` + `wheel`), and secure token handling.

---

### Step 1: Clone Your Empty GitHub Repo Locally

Open your terminal and clone your repository:

```bash
git clone git@github.com:deanagan/test-wheels.git
cd test-wheels

```

---

### Step 2: Initialize a Python Library Project with `uv`

Run `uv init` with the `--lib` flag inside your repository:

```bash
uv init --lib

```

This creates a standard Python package layout:

* `pyproject.toml` (Project metadata, dependencies, and build system configuration)
* `src/test_wheels/` (Where your library code lives)
* `src/test_wheels/__init__.py`
* `.python-version` & `.gitignore`

---

### Step 3: Add `numpy` as a Dependency

Add `numpy` to your library's `dependencies` list in `pyproject.toml`:

```bash
uv add numpy

```

---

### Step 4: Write the Calculator Code

Create `src/test_wheels/calculator.py` with your NumPy calculator logic:

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

Expose the `Calculator` class in `src/test_wheels/__init__.py`:

```python
from test_wheels.calculator import Calculator

__all__ = ["Calculator"]

```

---

### Step 5: Test Your Code Locally

Run a quick command in `uv`'s environment to verify functionality:

```bash
uv run python -c "from test_wheels import Calculator; print(Calculator.add([1, 2], [3, 4]))"

```

*Expected output: `[4.0, 6.0]*`

---

### Step 6: Build Your Packages (`wheel` + `sdist`)

Run `uv build` with `--no-sources`:

```bash
uv build --no-sources

```

#### Why these flags and outputs?

* **`--no-sources`**: Ignores any local path overrides or development source bindings configured in your `pyproject.toml`, ensuring the package relies purely on published PyPI dependencies.
* **Output files in `dist/**`:
* **Wheel (`.whl`)**: `dist/test_wheels-0.1.0-py3-none-any.whl` (The pre-built binary package for instant installation).
* **Source Distribution (`sdist`)**: `dist/test_wheels-0.1.0.tar.gz` (The raw source code fallback for platforms or build environments that cannot use the wheel).



---

### Step 7: Push Your Source Code to GitHub

Save your codebase to Git:

```bash
git add .
git commit -m "feat: setup library and add numpy calculator"
git push -u origin main

```

---

### Step 8: Securely Upload to PyPI / TestPyPI

To avoid leaking your API token on-screen or saving it into your shell history (`.bash_history`/`.zsh_history`), use environment variables or secure interactive prompts instead of passing `--token` directly in the command line.

#### Option A: Publish to **TestPyPI** (Recommended for Practice)

1. Create a free account on [TestPyPI](https://www.google.com/search?q=https://testpypi.org/account/register/&utm_source=gemini) and generate an API Token under **Account Settings -> API tokens**.
2. Set the token securely as an environment variable and publish:

```bash
export UV_PUBLISH_TOKEN="pypi-YOUR_TEST_PYPI_TOKEN"
uv publish --publish-url https://test.pypi.org/legacy/

```

3. **Verify Installation:** Test installing your published wheel in an isolated `uv` environment:

```bash
uv run --isolated --extra-index-url https://test.pypi.org/simple/ --with test-wheels python -c "from test_wheels import Calculator; print(Calculator.mean([10, 20, 30]))"

```

---

#### Option B: Publish to Real **PyPI**

1. Create an account on [PyPI.org](https://pypi.org/?utm_source=gemini) and generate an API Token under **Account Settings**.
2. Publish using interactive masked input (where typing is hidden from the screen):

```bash
uv publish

```

*`uv` will prompt you to securely paste your token without printing any characters.*

Alternatively, set the environment variable inline for that single execution:

```bash
UV_PUBLISH_TOKEN="pypi-YOUR_PYPI_TOKEN" uv publish

```

## Azure artifacts
To publish to or install from an **Azure Artifacts Python Feed** using `uv`, the workflow differs slightly from PyPI because Azure Artifacts requires specific upload URLs and authentication (either via Personal Access Token or Azure Keyring).

---

### Understanding the Azure Artifacts URLs

An Azure Artifacts Python Feed provides two separate URLs:

1. **Upload URL (for publishing):**
`[https://pkgs.dev.azure.com/](https://pkgs.dev.azure.com/)<ORGANIZATION>/<PROJECT>/_packaging/<FEED_NAME>/pypi/upload/`
2. **Index URL (for installing/consuming packages):**
`[https://pkgs.dev.azure.com/](https://pkgs.dev.azure.com/)<ORGANIZATION>/<PROJECT>/_packaging/<FEED_NAME>/pypi/simple/`

*(Note: If your feed is organization-scoped rather than project-scoped, omit `<PROJECT>` from the path).*

---

### Step 1: Set Up Authentication Options

Azure Artifacts requires authentication before accepts your wheels. You can authenticate using a **Personal Access Token (PAT)** or the **Azure Artifacts Credential Provider (`artifacts-keyring`)**.

#### Method A: Personal Access Token (PAT) — *Simplest for Local & CI/CD*

1. In Azure DevOps, go to **User Settings** (top right) $\rightarrow$ **Personal Access Tokens**.
2. Click **New Token**, grant the **Packaging (Read & Write)** scope, and copy the token.
3. Export the token as an environment variable in your terminal:

```bash
export AZURE_ARTIFACTS_PAT="your-copied-pat-token"

```

#### Method B: Interactive Login via `keyring` — *Best for local interactive development*

If you don't want to manage PAT expiration dates manually, `uv` supports Azure's `artifacts-keyring` authentication plugin:

```bash
# Install keyring and Microsoft's Azure Artifacts plugin globally via uv
uv tool install keyring --with artifacts-keyring

# Enable keyring support in uv
export UV_KEYRING_PROVIDER=subprocess
export UV_INDEX_PRIVATE_REGISTRY_USERNAME=VssSessionToken

```

---

### Step 2: Build Your Packages

As always, run `uv build` with `--no-sources` to ensure no local file path overrides leak into your production wheel:

```bash
uv build --no-sources

```

---

### Step 3: Publish to Azure Artifacts

Use `uv publish` pointing directly to your feed's **upload** endpoint.

#### Using a PAT (Method A):

Azure Artifacts expects HTTP Basic Authentication where the username can be any string (e.g., `AZURE_DEVOPS`) and the password is your PAT.

```bash
UV_PUBLISH_USERNAME="AZURE_DEVOPS" \
UV_PUBLISH_TOKEN="$AZURE_ARTIFACTS_PAT" \
uv publish --publish-url https://pkgs.dev.azure.com/YOUR_ORG/YOUR_PROJECT/_packaging/YOUR_FEED/pypi/upload/

```

#### Using Keyring (Method B):

When `UV_KEYRING_PROVIDER=subprocess` is set, `uv publish` delegates authentication to `artifacts-keyring`, which will prompt a browser login if you are not logged in:

```bash
uv publish --publish-url https://pkgs.dev.azure.com/YOUR_ORG/YOUR_PROJECT/_packaging/YOUR_FEED/pypi/upload/

```

---

### Step 4: Configure Your Project to Install from Azure Artifacts

To allow yourself or teammates to install your package from Azure Artifacts using `uv`, register your feed's **index** URL (`/pypi/simple/`) in your `pyproject.toml`:

#### 1. Add the Index to `pyproject.toml`

```toml
[[tool.uv.index]]
name = "azure-feed"
url = "https://pkgs.dev.azure.com/YOUR_ORG/YOUR_PROJECT/_packaging/YOUR_FEED/pypi/simple/"

```

#### 2. Install Your Package using `uv`

When running `uv pip install` or `uv add`, pass the PAT credentials securely via environment variables:

```bash
# Pass credentials via environment variable
UV_INDEX_AZURE_FEED_USERNAME="AZURE_DEVOPS" \
UV_INDEX_AZURE_FEED_PASSWORD="$AZURE_ARTIFACTS_PAT" \
uv run --isolated --with test-wheels python -c "from test_wheels import Calculator; print(Calculator.mean([10, 20, 30]))"

```

---

### Summary Checklist for Azure Artifacts

| Action | Command / Configuration |
| --- | --- |
| **Build** | `uv build --no-sources` |
| **Publish (PAT)** | `UV_PUBLISH_USERNAME="user" UV_PUBLISH_TOKEN="PAT" uv publish --publish-url <UPLOAD_URL>` |
| **Publish (Keyring)** | `export UV_KEYRING_PROVIDER=subprocess`<br>

<br>`uv publish --publish-url <UPLOAD_URL>` |
| **Install** | Add `[[tool.uv.index]]` to `pyproject.toml`, then `uv add test-wheels` |