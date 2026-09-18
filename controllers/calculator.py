from flask import Blueprint, jsonify, request


def sum_numbers(a: float, b: float) -> float:
    """Pure function: returns the sum of two numbers (int or float)."""
    return a + b


calculator_bp = Blueprint("calculator", __name__)


@calculator_bp.route("/sum", methods=["GET"])
def sum_route():
    """Сумма двух чисел
    ---
    parameters:
      - name: a
        in: query
        type: number
        required: true
        description: Первое слагаемое
      - name: b
        in: query
        type: number
        required: true
        description: Второе слагаемое
    responses:
      200:
        description: Результат сложения
        schema:
          type: object
          properties:
            result:
              type: number
      400:
        description: Неверные параметры (отсутствуют или не числа)
    """
    a_str = request.args.get("a")
    b_str = request.args.get("b")
    if a_str is None or b_str is None:
        return jsonify({"error": "Missing parameters: a and b are required"}), 400
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        return jsonify({"error": "a and b must be numbers"}), 400
    result = sum_numbers(a, b)
    return jsonify({"result": result})
