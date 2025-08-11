"""
Test cases for Calculator module following TDD approach.
"""

import math
from typing import Any

import pytest

from src.example_calculator import (
    Calculator,
    DivisionByZeroError,
    InvalidOperationError,
)


class TestCalculatorBasicOperations:
    """Test basic arithmetic operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        """Test addition of positive numbers."""
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(0, 0) == 0
        assert self.calc.add(100, 200) == 300

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        assert self.calc.add(-2, -3) == -5
        assert self.calc.add(-5, 5) == 0
        assert self.calc.add(10, -15) == -5

    def test_add_floats(self):
        """Test addition with floating point numbers."""
        assert self.calc.add(1.5, 2.5) == 4.0
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)
        assert self.calc.add(-1.5, 1.5) == 0.0

    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers."""
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(10, 10) == 0
        assert self.calc.subtract(0, 5) == -5

    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        assert self.calc.subtract(-5, -3) == -2
        assert self.calc.subtract(-5, 5) == -10
        assert self.calc.subtract(5, -5) == 10

    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers."""
        assert self.calc.multiply(3, 4) == 12
        assert self.calc.multiply(0, 100) == 0
        assert self.calc.multiply(1, 50) == 50

    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers."""
        assert self.calc.multiply(-3, 4) == -12
        assert self.calc.multiply(-3, -4) == 12
        assert self.calc.multiply(0, -5) == 0

    def test_multiply_floats(self):
        """Test multiplication with floating point numbers."""
        assert self.calc.multiply(1.5, 2.0) == 3.0
        assert self.calc.multiply(0.1, 0.1) == pytest.approx(0.01)

    def test_divide_positive_numbers(self):
        """Test division of positive numbers."""
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(7, 2) == 3.5
        assert self.calc.divide(1, 1) == 1

    def test_divide_negative_numbers(self):
        """Test division with negative numbers."""
        assert self.calc.divide(-10, 2) == -5
        assert self.calc.divide(10, -2) == -5
        assert self.calc.divide(-10, -2) == 5

    def test_divide_by_zero_raises_error(self):
        """Test that division by zero raises appropriate error."""
        with pytest.raises(DivisionByZeroError) as exc_info:
            self.calc.divide(10, 0)
        assert "Cannot divide by zero" in str(exc_info.value)


class TestCalculatorAdvancedOperations:
    """Test advanced mathematical operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_power_positive_exponent(self):
        """Test power operation with positive exponent."""
        assert self.calc.power(2, 3) == 8
        assert self.calc.power(5, 2) == 25
        assert self.calc.power(10, 0) == 1

    def test_power_negative_exponent(self):
        """Test power operation with negative exponent."""
        assert self.calc.power(2, -1) == 0.5
        assert self.calc.power(4, -2) == 0.0625

    def test_power_fractional_exponent(self):
        """Test power operation with fractional exponent."""
        assert self.calc.power(4, 0.5) == 2
        assert self.calc.power(27, 1 / 3) == pytest.approx(3)

    def test_sqrt_positive_numbers(self):
        """Test square root of positive numbers."""
        assert self.calc.sqrt(4) == 2
        assert self.calc.sqrt(9) == 3
        assert self.calc.sqrt(2) == pytest.approx(math.sqrt(2))

    def test_sqrt_zero(self):
        """Test square root of zero."""
        assert self.calc.sqrt(0) == 0

    def test_sqrt_negative_raises_error(self):
        """Test that square root of negative number raises error."""
        with pytest.raises(InvalidOperationError) as exc_info:
            self.calc.sqrt(-1)
        assert "Cannot calculate square root of negative number" in str(exc_info.value)

    def test_factorial_positive_integers(self):
        """Test factorial of positive integers."""
        assert self.calc.factorial(0) == 1
        assert self.calc.factorial(1) == 1
        assert self.calc.factorial(5) == 120
        assert self.calc.factorial(10) == 3628800

    def test_factorial_negative_raises_error(self):
        """Test that factorial of negative number raises error."""
        with pytest.raises(InvalidOperationError) as exc_info:
            self.calc.factorial(-1)
        assert "Factorial is not defined for negative numbers" in str(exc_info.value)

    def test_factorial_non_integer_raises_error(self):
        """Test that factorial of non-integer raises error."""
        with pytest.raises(InvalidOperationError) as exc_info:
            self.calc.factorial(3.5)
        assert "Factorial is only defined for integers" in str(exc_info.value)


class TestCalculatorMemoryOperations:
    """Test calculator memory functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_memory_store_and_recall(self):
        """Test storing and recalling values from memory."""
        self.calc.memory_store(42)
        assert self.calc.memory_recall() == 42

    def test_memory_add(self):
        """Test adding to memory."""
        self.calc.memory_store(10)
        self.calc.memory_add(5)
        assert self.calc.memory_recall() == 15

    def test_memory_subtract(self):
        """Test subtracting from memory."""
        self.calc.memory_store(10)
        self.calc.memory_subtract(3)
        assert self.calc.memory_recall() == 7

    def test_memory_clear(self):
        """Test clearing memory."""
        self.calc.memory_store(100)
        self.calc.memory_clear()
        assert self.calc.memory_recall() == 0

    def test_memory_recall_empty(self):
        """Test recalling from empty memory."""
        assert self.calc.memory_recall() == 0


class TestCalculatorChainOperations:
    """Test method chaining functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_chain_operations(self):
        """Test chaining multiple operations."""
        result = (
            self.calc.chain(10)
            .chain_add(5)
            .chain_multiply(2)
            .chain_subtract(10)
            .chain_divide(4)
            .get_result()
        )
        assert result == 5.0

    def test_chain_with_power(self):
        """Test chaining with power operation."""
        result = self.calc.chain(2).chain_power(3).chain_add(2).get_result()
        assert result == 10

    def test_chain_reset(self):
        """Test resetting chain."""
        self.calc.chain(100).chain_add(50)
        self.calc.reset_chain()
        result = self.calc.chain(5).chain_multiply(3).get_result()
        assert result == 15


class TestCalculatorInputValidation:
    """Test input validation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    @pytest.mark.parametrize(
        ("a", "b"),
        [
            ("5", 3),
            (5, "3"),
            ("5", "3"),
            (None, 5),
            (5, None),
            ([], 5),
            ({}, 5),
        ],
    )
    def test_add_invalid_types(self, a: Any, b: Any):
        """Test that invalid types raise TypeError."""
        with pytest.raises(TypeError):
            self.calc.add(a, b)

    @pytest.mark.parametrize(
        ("a", "b"),
        [
            (float("inf"), 1),
            (1, float("inf")),
            (float("-inf"), 1),
            (float("nan"), 1),
            (1, float("nan")),
        ],
    )
    def test_operations_with_special_floats(self, a: float, b: float):
        """Test operations with special float values."""
        # These should not raise errors but handle gracefully
        if not math.isnan(a) and not math.isnan(b):
            result = self.calc.add(a, b)
            # Just verify it doesn't crash
            assert result is not None


class TestCalculatorConstants:
    """Test mathematical constants."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_pi_constant(self):
        """Test PI constant value."""
        assert self.calc.get_pi() == pytest.approx(math.pi)

    def test_e_constant(self):
        """Test E constant value."""
        assert self.calc.get_e() == pytest.approx(math.e)


class TestCalculatorStatistics:
    """Test statistical operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def test_mean(self):
        """Test mean calculation."""
        assert self.calc.mean([1, 2, 3, 4, 5]) == 3
        assert self.calc.mean([10, 20]) == 15
        assert self.calc.mean([5]) == 5

    def test_mean_empty_list(self):
        """Test mean of empty list raises error."""
        with pytest.raises(InvalidOperationError):
            self.calc.mean([])

    def test_median(self):
        """Test median calculation."""
        assert self.calc.median([1, 2, 3, 4, 5]) == 3
        assert self.calc.median([1, 2, 3, 4]) == 2.5
        assert self.calc.median([5]) == 5

    def test_mode(self):
        """Test mode calculation."""
        assert self.calc.mode([1, 2, 2, 3, 3, 3]) == 3
        assert self.calc.mode([1, 1, 2, 2]) in [1, 2]  # Both are valid
        assert self.calc.mode([5]) == 5


@pytest.mark.unit()
class TestCalculatorUnitTests:
    """Marker for unit tests."""

    def test_calculator_creation(self):
        """Test calculator instance creation."""
        calc = Calculator()
        assert calc is not None
        assert hasattr(calc, "add")
        assert hasattr(calc, "subtract")
        assert hasattr(calc, "multiply")
        assert hasattr(calc, "divide")


@pytest.mark.integration()
class TestCalculatorIntegration:
    """Integration tests for calculator."""

    def test_complex_calculation(self):
        """Test complex multi-step calculation."""
        calc = Calculator()
        # (10 + 5) * 2 - 8 / 4
        step1 = calc.add(10, 5)  # 15
        step2 = calc.multiply(step1, 2)  # 30
        step3 = calc.divide(8, 4)  # 2
        result = calc.subtract(step2, step3)  # 28
        assert result == 28
