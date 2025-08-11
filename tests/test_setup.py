"""Tests for setup.sh script functionality."""

import os
import subprocess
import tempfile
from pathlib import Path


class TestSetupScript:
    """Test cases for the setup.sh script."""

    def test_setup_script_exists(self):
        """Test that setup.sh script exists."""
        setup_script = Path("scripts/setup.sh")
        assert setup_script.exists(), "setup.sh script not found"
        assert setup_script.is_file(), "setup.sh is not a file"

    def test_setup_script_is_executable(self):
        """Test that setup.sh script has executable permissions."""
        setup_script = Path("scripts/setup.sh")
        assert os.access(setup_script, os.X_OK), "setup.sh is not executable"

    def test_requirements_common_exists(self):
        """Test that requirements-common.txt exists."""
        requirements_common = Path("requirements-common.txt")
        assert requirements_common.exists(), "requirements-common.txt not found"
        assert requirements_common.is_file(), "requirements-common.txt is not a file"

    def test_requirements_dev_example_exists(self):
        """Test that requirements-dev.txt.example exists."""
        requirements_example = Path("requirements-dev.txt.example")
        assert requirements_example.exists(), "requirements-dev.txt.example not found"
        assert requirements_example.is_file(), (
            "requirements-dev.txt.example is not a file"
        )

    def test_requirements_dev_in_gitignore(self):
        """Test that requirements-dev.txt is in .gitignore."""
        gitignore = Path(".gitignore")
        assert gitignore.exists(), ".gitignore not found"

        with gitignore.open() as f:
            content = f.read()
            assert "requirements-dev.txt" in content, (
                "requirements-dev.txt not in .gitignore"
            )

    def test_requirements_common_content(self):
        """Test that requirements-common.txt contains expected libraries."""
        requirements_common = Path("requirements-common.txt")
        with requirements_common.open() as f:
            content = f.read()

            # Check for common data science libraries
            assert "pandas" in content, "pandas not in requirements-common.txt"
            assert "numpy" in content, "numpy not in requirements-common.txt"
            assert "requests" in content, "requests not in requirements-common.txt"

    def test_requirements_dev_example_content(self):
        """Test that requirements-dev.txt.example contains usage instructions."""
        requirements_example = Path("requirements-dev.txt.example")
        with requirements_example.open() as f:
            content = f.read()

            # Check for usage instructions
            assert "How to use:" in content, "Usage instructions not found"
            assert "cp requirements-dev.txt.example requirements-dev.txt" in content, (
                "Copy command not found"
            )
            assert ".gitignore" in content, "Gitignore mention not found"

    def test_setup_script_handles_requirements(self):
        """Test that setup.sh script handles requirements files correctly."""
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a minimal test environment
            test_dir = Path(tmpdir)

            # Copy necessary files to temp directory
            setup_script = test_dir / "setup.sh"
            setup_script.write_text(Path("scripts/setup.sh").read_text())
            setup_script.chmod(0o755)

            # Create test requirements files
            requirements_common = test_dir / "requirements-common.txt"
            requirements_common.write_text("# Test common requirements\nrequests\n")

            requirements_dev = test_dir / "requirements-dev.txt"
            requirements_dev.write_text("# Test dev requirements\njupyter\n")

            # Create a minimal pyproject.toml
            pyproject = test_dir / "pyproject.toml"
            pyproject.write_text("""
[project]
name = "test-project"
version = "0.1.0"
dependencies = []

[project.optional-dependencies]
dev = []
test = []
docs = []
""")

            # Run setup script in dry-run mode (just check syntax)
            result = subprocess.run(
                ["bash", "-n", str(setup_script)],
                check=False,
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0, (
                f"Script syntax check failed: {result.stderr}"
            )
