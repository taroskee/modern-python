"""
Calculator module implementing basic and advanced mathematical operations.

This module provides a Calculator class with various mathematical operations
including basic arithmetic, advanced functions, memory operations, and
statistical calculations.
"""

import math
from typing import Any


Number = int | float


class CalculatorError(Exception):
    """Base exception for calculator-related errors."""


class DivisionByZeroError(CalculatorError):
    """Exception raised when attempting to divide by zero."""


class InvalidOperationError(CalculatorError):
    """Exception raised for invalid mathematical operations."""


class Calculator:
    """
    A calculator class providing various mathematical operations.

    This class implements basic arithmetic operations, advanced mathematical
    functions, memory operations, and method chaining for complex calculations.

    Attributes:
        memory: Stores a value for memory operations
        chain_value: Current value in chain operations
    """

    def __init__(self):
        """Initialize calculator with memory and chain value."""
        self.memory: float = 0
        self.chain_value: float | None = None

    # Basic arithmetic operations

    def add(self, a: Number, b: Number) -> float:
        """
        Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b

        Raises:
            TypeError: If arguments are not numbers
        """
        self._validate_numbers(a, b)
        return float(a + b)

    def subtract(self, a: Number, b: Number) -> float:
        """
        Subtract b from a.

        Args:
            a: Minuend
            b: Subtrahend

        Returns:
            Difference of a and b

        Raises:
            TypeError: If arguments are not numbers
        """
        self._validate_numbers(a, b)
        return float(a - b)

    def multiply(self, a: Number, b: Number) -> float:
        """
        Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Product of a and b

        Raises:
            TypeError: If arguments are not numbers
        """
        self._validate_numbers(a, b)
        return float(a * b)

    def divide(self, a: Number, b: Number) -> float:
        """
        Divide a by b.

        Args:
            a: Dividend
            b: Divisor

        Returns:
            Quotient of a and b

        Raises:
            TypeError: If arguments are not numbers
            DivisionByZeroError: If b is zero
        """
        self._validate_numbers(a, b)
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return float(a / b)

    # Advanced mathematical operations

    def power(self, base: Number, exponent: Number) -> float:
        """
        Raise base to the power of exponent.

        Args:
            base: Base number
            exponent: Exponent

        Returns:
            base raised to the power of exponent

        Raises:
            TypeError: If arguments are not numbers
        """
        self._validate_numbers(base, exponent)
        return float(base**exponent)

    def sqrt(self, n: Number) -> float:
        """
        Calculate square root of a number.

        Args:
            n: Number to calculate square root of

        Returns:
            Square root of n

        Raises:
            TypeError: If argument is not a number
            InvalidOperationError: If n is negative
        """
        self._validate_number(n)
        if n < 0:
            raise InvalidOperationError(
                "Cannot calculate square root of negative number",
            )
        return math.sqrt(n)

    def factorial(self, n: Number) -> int:
        """
        Calculate factorial of a non-negative integer.

        Args:
            n: Non-negative integer

        Returns:
            Factorial of n

        Raises:
            TypeError: If argument is not a number
            InvalidOperationError: If n is negative or not an integer
        """
        self._validate_number(n)
        if n < 0:
            raise InvalidOperationError("Factorial is not defined for negative numbers")
        if not isinstance(n, int) and not n.is_integer():
            raise InvalidOperationError("Factorial is only defined for integers")
        return math.factorial(int(n))

    # Memory operations

    def memory_store(self, value: Number) -> None:
        """
        Store a value in memory.

        Args:
            value: Value to store

        Raises:
            TypeError: If value is not a number
        """
        self._validate_number(value)
        self.memory = float(value)

    def memory_recall(self) -> float:
        """
        Recall value from memory.

        Returns:
            Value stored in memory
        """
        return self.memory

    def memory_add(self, value: Number) -> None:
        """
        Add value to memory.

        Args:
            value: Value to add to memory

        Raises:
            TypeError: If value is not a number
        """
        self._validate_number(value)
        self.memory += value

    def memory_subtract(self, value: Number) -> None:
        """
        Subtract value from memory.

        Args:
            value: Value to subtract from memory

        Raises:
            TypeError: If value is not a number
        """
        self._validate_number(value)
        self.memory -= value

    def memory_clear(self) -> None:
        """Clear memory (set to 0)."""
        self.memory = 0

    # Chain operations

    def chain(self, initial: Number) -> "Calculator":
        """
        Start a chain of operations with an initial value.

        Args:
            initial: Initial value for chain

        Returns:
            Self for method chaining

        Raises:
            TypeError: If initial is not a number
        """
        self._validate_number(initial)
        self.chain_value = float(initial)
        return self

    def chain_add(self, value: Number) -> "Calculator":
        """
        Add value in chain operation.

        Args:
            value: Value to add

        Returns:
            Self for method chaining

        Raises:
            TypeError: If value is not a number
            InvalidOperationError: If chain not initialized
        """
        self._ensure_chain_initialized()
        self._validate_number(value)
        self.chain_value += value
        return self

    def chain_subtract(self, value: Number) -> "Calculator":
        """
        Subtract value in chain operation.

        Args:
            value: Value to subtract

        Returns:
            Self for method chaining

        Raises:
            TypeError: If value is not a number
            InvalidOperationError: If chain not initialized
        """
        self._ensure_chain_initialized()
        self._validate_number(value)
        self.chain_value -= value
        return self

    def chain_multiply(self, value: Number) -> "Calculator":
        """
        Multiply by value in chain operation.

        Args:
            value: Value to multiply by

        Returns:
            Self for method chaining

        Raises:
            TypeError: If value is not a number
            InvalidOperationError: If chain not initialized
        """
        self._ensure_chain_initialized()
        self._validate_number(value)
        self.chain_value *= value
        return self

    def chain_divide(self, value: Number) -> "Calculator":
        """
        Divide by value in chain operation.

        Args:
            value: Value to divide by

        Returns:
            Self for method chaining

        Raises:
            TypeError: If value is not a number
            DivisionByZeroError: If value is zero
            InvalidOperationError: If chain not initialized
        """
        self._ensure_chain_initialized()
        self._validate_number(value)
        if value == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        self.chain_value /= value
        return self

    def chain_power(self, value: Number) -> "Calculator":
        """
        Raise to power in chain operation.

        Args:
            value: Exponent

        Returns:
            Self for method chaining

        Raises:
            TypeError: If value is not a number
            InvalidOperationError: If chain not initialized
        """
        self._ensure_chain_initialized()
        self._validate_number(value)
        self.chain_value **= value
        return self

    def get_result(self) -> float:
        """
        Get the result of chain operations.

        Returns:
            Current chain value

        Raises:
            InvalidOperationError: If chain not initialized
        """
        self._ensure_chain_initialized()
        return self.chain_value

    def reset_chain(self) -> None:
        """Reset chain operations."""
        self.chain_value = None

    # Mathematical constants

    @staticmethod
    def get_pi() -> float:
        """
        Get the value of pi.

        Returns:
            Value of pi
        """
        return math.pi

    @staticmethod
    def get_e() -> float:
        """
        Get the value of e (Euler's number).

        Returns:
            Value of e
        """
        return math.e

    # Statistical operations

    def mean(self, numbers: list[Number]) -> float:
        """
        Calculate arithmetic mean of a list of numbers.

        Args:
            numbers: List of numbers

        Returns:
            Arithmetic mean

        Raises:
            InvalidOperationError: If list is empty
            TypeError: If list contains non-numbers
        """
        if not numbers:
            raise InvalidOperationError("Cannot calculate mean of empty list")
        for num in numbers:
            self._validate_number(num)
        return sum(numbers) / len(numbers)

    def median(self, numbers: list[Number]) -> float:
        """
        Calculate median of a list of numbers.

        Args:
            numbers: List of numbers

        Returns:
            Median value

        Raises:
            InvalidOperationError: If list is empty
            TypeError: If list contains non-numbers
        """
        if not numbers:
            raise InvalidOperationError("Cannot calculate median of empty list")
        for num in numbers:
            self._validate_number(num)

        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)

        if n % 2 == 0:
            return (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
        return sorted_numbers[n // 2]

    def mode(self, numbers: list[Number]) -> Number:
        """
        Calculate mode of a list of numbers.

        Args:
            numbers: List of numbers

        Returns:
            Most frequent value

        Raises:
            InvalidOperationError: If list is empty
            TypeError: If list contains non-numbers
        """
        if not numbers:
            raise InvalidOperationError("Cannot calculate mode of empty list")
        for num in numbers:
            self._validate_number(num)

        frequency = {}
        for num in numbers:
            frequency[num] = frequency.get(num, 0) + 1

        max_count = max(frequency.values())
        modes = [num for num, count in frequency.items() if count == max_count]

        return modes[0]  # Return first mode if multiple exist

    # Helper methods

    def _validate_number(self, value: Any) -> None:
        """
        Validate that a value is a number.

        Args:
            value: Value to validate

        Raises:
            TypeError: If value is not a number
        """
        if not isinstance(value, int | float):
            raise TypeError(f"Expected number, got {type(value).__name__}")

    def _validate_numbers(self, *values: Any) -> None:
        """
        Validate that multiple values are numbers.

        Args:
            *values: Values to validate

        Raises:
            TypeError: If any value is not a number
        """
        for value in values:
            self._validate_number(value)

    def _ensure_chain_initialized(self) -> None:
        """
        Ensure chain operations have been initialized.

        Raises:
            InvalidOperationError: If chain not initialized
        """
        if self.chain_value is None:
            raise InvalidOperationError("Chain not initialized. Call chain() first.")
