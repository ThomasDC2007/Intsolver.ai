from flask import Flask, request, render_template, jsonify
import sympy as sp

app = Flask(__name__)

def solve_integral(integral_expr, lower=None, upper=None):
    x = sp.symbols('x')
    expr = sp.sympify(integral_expr)
    steps = []

    # Step 1: Display the integral
    if lower is not None and upper is not None:
        steps.append(f"Step 1: The integral to solve is: \\( \\int_{{{lower}}}^{{{upper}}} {sp.latex(expr)} \\, dx \\)")
    else:
        steps.append(f"Step 1: The integral to solve is: \\( \\int {sp.latex(expr)} \\, dx \\)")

    # Step 2: Choose the appropriate integration method
    if expr.is_polynomial():
        steps.append("Step 2: Using basic integral formulas.")
        integral = sp.integrate(expr, x)
    elif expr.has(sp.sin, sp.cos):
        steps.append("Step 2: Using trigonometric integrals.")
        integral = sp.integrate(expr, x)
    elif expr.is_rational_function():
        steps.append("Step 2: Using partial fraction decomposition.")
        integral = sp.integrate(expr, x)
    else:
        steps.append("Step 2: Using general integration techniques.")
        integral = sp.integrate(expr, x)

    # Step 3: Compute the integral
    if lower is not None and upper is not None:
        definite_integral = sp.integrate(expr, (x, lower, upper))
        steps.append(f"Step 3: Compute the definite integral.")
        steps.append(f"\\( \\int_{{{lower}}}^{{{upper}}} {sp.latex(expr)} \\, dx = {sp.latex(definite_integral)} \\)")
    else:
        steps.append(f"Step 3: Compute the indefinite integral.")
        steps.append(f"\\( \\int {sp.latex(expr)} \\, dx = {sp.latex(integral)} + C \\)")

    # Step 4: Simplify the result
    simplified_integral = sp.simplify(integral)
    if simplified_integral != integral:
        steps.append(f"Step 4: Simplify the result.")
        steps.append(f"\\( {sp.latex(integral)} + C \\) simplifies to \\( {sp.latex(simplified_integral)} + C \\)")

    # Step 5: Final result
    steps.append(f"Step 5: Final result:")
    if lower is not None and upper is not None:
        steps.append(f"\\( \\int_{{{lower}}}^{{{upper}}} {sp.latex(expr)} \\, dx = {sp.latex(definite_integral)} \\)")
    else:
        steps.append(f"\\( \\int {sp.latex(expr)} \\, dx = {sp.latex(simplified_integral)} + C \\)")

    return steps

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    integral_expr = data.get("integral")
    lower = data.get("lower")
    upper = data.get("upper")
    try:
        steps = solve_integral(integral_expr, lower, upper)
        return jsonify({"success": True, "steps": steps})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)