API Reference
=============

このセクションでは、Modern Pythonプロジェクトの全APIリファレンスを提供します。

.. contents::
   :local:
   :depth: 2

Core Modules
------------

Calculator Module
~~~~~~~~~~~~~~~~~

.. automodule:: src.example_calculator
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Example Usage
^^^^^^^^^^^^^

基本的な計算機能の使用例:

.. code-block:: python

    from src.example_calculator import Calculator
    
    # Create calculator instance
    calc = Calculator()
    
    # Basic operations
    result = calc.add(10, 5)        # 15
    result = calc.subtract(10, 5)   # 5
    result = calc.multiply(10, 5)   # 50
    result = calc.divide(10, 5)     # 2.0
    
    # Advanced operations
    result = calc.power(2, 8)       # 256
    result = calc.sqrt(16)          # 4.0

API Classes
-----------

Calculator Class
~~~~~~~~~~~~~~~~

.. class:: Calculator

   基本的な算術演算を提供するクラス。

   .. method:: add(a: float, b: float) -> float
   
      2つの数値を加算します。
      
      :param a: 第1引数
      :param b: 第2引数
      :return: a + b の結果
      :raises TypeError: 引数が数値でない場合
      
      **Example:**
      
      .. code-block:: python
      
         >>> calc = Calculator()
         >>> calc.add(3, 4)
         7

   .. method:: subtract(a: float, b: float) -> float
   
      第1引数から第2引数を減算します。
      
      :param a: 被減数
      :param b: 減数
      :return: a - b の結果
      :raises TypeError: 引数が数値でない場合

   .. method:: multiply(a: float, b: float) -> float
   
      2つの数値を乗算します。
      
      :param a: 第1引数
      :param b: 第2引数
      :return: a × b の結果
      :raises TypeError: 引数が数値でない場合

   .. method:: divide(a: float, b: float) -> float
   
      第1引数を第2引数で除算します。
      
      :param a: 被除数
      :param b: 除数
      :return: a ÷ b の結果
      :raises TypeError: 引数が数値でない場合
      :raises ZeroDivisionError: 除数が0の場合

   .. method:: power(base: float, exponent: float) -> float
   
      基数を指定された指数でべき乗します。
      
      :param base: 基数
      :param exponent: 指数
      :return: base^exponent の結果
      :raises TypeError: 引数が数値でない場合

   .. method:: sqrt(n: float) -> float
   
      数値の平方根を計算します。
      
      :param n: 平方根を求める数値
      :return: √n の結果
      :raises TypeError: 引数が数値でない場合
      :raises ValueError: 負の数の場合

Exceptions
----------

.. exception:: CalculatorError

   Calculator関連のエラーの基底クラス。

.. exception:: DivisionByZeroError(CalculatorError)

   ゼロ除算が発生した場合に発生する例外。

.. exception:: InvalidOperationError(CalculatorError)

   無効な操作が実行された場合に発生する例外。

Type Definitions
----------------

.. data:: Number

   計算で使用可能な数値型のユニオン型。
   
   .. code-block:: python
   
      from typing import Union
      
      Number = Union[int, float]

Constants
---------

.. data:: PI
   :type: float
   :value: 3.14159265359

   円周率の定数。

.. data:: E
   :type: float
   :value: 2.71828182846

   自然対数の底の定数。

Utilities
---------

.. function:: validate_number(value: Any) -> bool

   値が有効な数値かどうかを検証します。
   
   :param value: 検証する値
   :return: 数値の場合True、それ以外はFalse

.. function:: round_to_precision(value: float, precision: int = 2) -> float

   数値を指定された精度に丸めます。
   
   :param value: 丸める値
   :param precision: 小数点以下の桁数
   :return: 丸められた値