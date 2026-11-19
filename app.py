
import os
from decimal import Decimal, InvalidOperation
from datetime import date
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, UserMixin, login_user,
    logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

# Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User model
class User(UserMixin):
    def __init__(self, user_id, username, role, business_id):
        self.id = user_id
        self.username = username
        self.role = role
        self.business_id = business_id


@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT user_id, username, role, business_id FROM users WHERE user_id=%s",
            (user_id,)
        )
        user = cur.fetchone()

        if user:
            return User(
                user["user_id"],
                user["username"],
                user["role"],
                user["business_id"]
            )
        return None
    finally:
        cur.close()
        conn.close()


# Database helpers
def query_all(sql, params=()):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def query_one(sql, params=()):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


# Admin permission decorator
def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            flash("You do not have access to this page.", "error")
            return redirect(url_for("dashboard"))
        return func(*args, **kwargs)
    return wrapper


# First-time administrator setup
@app.route("/setup-admin", methods=["GET", "POST"])
def setup_admin():
    count = query_one("SELECT COUNT(*) AS total FROM users")

    if count["total"] > 0:
        flash("An administrator account has already been created.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if len(username) < 3 or len(password) < 8:
            flash("Username must have 3 characters and password at least 8.", "error")
            return render_template("setup_admin.html")

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("setup_admin.html")

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
INSERT INTO users (username, password_hash, role, business_id)
VALUES (%s, %s, %s, %s)
""",
                (username, generate_password_hash(password), "admin" , 1)
            )
            conn.commit()
            flash("Administrator account created. Please log in.", "success")
            return redirect(url_for("login"))
        except Exception:
            conn.rollback()
            flash("Could not create account. The username may already exist.", "error")
        finally:
            cur.close()
            conn.close()

    return render_template("setup_admin.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    count = query_one("SELECT COUNT(*) AS total FROM users")

    if count["total"] == 0:
        return redirect(url_for("setup_admin"))

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = query_one(
    """
    SELECT user_id, username, password_hash, role, business_id
    FROM users
    WHERE username=%s
    """,
    (username,)
)

        if user and check_password_hash(user["password_hash"], password):
            login_user(User(
    user["user_id"],
    user["username"],
    user["role"],
    user["business_id"]
))
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


# Logout
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("login"))


# Dashboard

@app.route("/")
@login_required
def dashboard():
    # Dashboard statistics for the logged-in business
    stats = query_one("""
        SELECT
            (SELECT COUNT(*)
             FROM products
             WHERE business_id=%s) AS total_products,

            (SELECT COALESCE(SUM(quantity), 0)
             FROM products
             WHERE business_id=%s) AS total_stock,

            (SELECT COUNT(*)
             FROM products
             WHERE quantity <= low_stock_limit
             AND business_id=%s) AS low_stock,

            (SELECT COALESCE(SUM(total_amount), 0)
             FROM sales
             WHERE business_id=%s) AS total_sales
    """, (
        current_user.business_id,
        current_user.business_id,
        current_user.business_id,
        current_user.business_id
    ))

    # Recent sales for this business only
    recent = query_all("""
        SELECT s.sale_id, p.product_name, s.quantity_sold,
               s.total_amount, s.sale_date
        FROM sales s
        JOIN products p ON p.product_id = s.product_id
        WHERE s.business_id=%s
        ORDER BY s.sale_date DESC, s.sale_id DESC
        LIMIT 6
    """, (current_user.business_id,))

    # Low-stock products for this business only
    low = query_all("""
        SELECT product_name, quantity, low_stock_limit
        FROM products
        WHERE quantity <= low_stock_limit
          AND business_id=%s
        ORDER BY quantity
        LIMIT 5
    """, (current_user.business_id,))

    return render_template(
        "dashboard.html", stats=stats, recent=recent, low=low
    )



# View products - Admin and Staff
@app.route("/products")
@login_required
def products():
    q = request.args.get("q", "").strip()

    if q:
        items = query_all(
            """
            SELECT * FROM products
            WHERE business_id = %s
            AND (product_name LIKE %s OR category LIKE %s)
            ORDER BY product_id DESC
            """,
            (current_user.business_id, f"%{q}%", f"%{q}%")
        )
    else:
        items = query_all(
            """
            SELECT * FROM products
            WHERE business_id = %s
            ORDER BY product_id DESC
            """,
            (current_user.business_id,)
        )

    return render_template("products.html", products=items, q=q)


# Add product - Admin only
@app.route("/products/add", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        try:
            name = request.form["product_name"].strip()
            category = request.form.get("category", "").strip()
            price = Decimal(request.form["price"])
            qty = int(request.form["quantity"])
            limit = int(request.form.get("low_stock_limit", 5))

            if not name or price < 0 or qty < 0 or limit < 0:
                raise ValueError()

        except (KeyError, ValueError, InvalidOperation):
            flash("Enter valid product details.", "error")
            return render_template(
                "product_form.html", product=request.form, mode="Add"
            )

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
    INSERT INTO products
    (product_name, category, price, quantity, low_stock_limit, business_id)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (
    name,
    category,
    price,
    qty,
    limit,
    current_user.business_id
))
            conn.commit()
            flash("Product added successfully.", "success")
        except Exception:
            conn.rollback()
            flash("Could not add product.", "error")
        finally:
            cur.close()
            conn.close()

        return redirect(url_for("products"))

    return render_template("product_form.html", product={}, mode="Add")


# Edit product - Admin only
@app.route("/products/edit/<int:pid>", methods=["GET", "POST"])
@admin_required
def edit_product(pid):
    product = query_one(
    """
    SELECT * FROM products
    WHERE product_id=%s AND business_id=%s
    """,
    (pid, current_user.business_id)
)

    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products"))

    if request.method == "POST":
        try:
            name = request.form["product_name"].strip()
            category = request.form.get("category", "").strip()
            price = Decimal(request.form["price"])
            qty = int(request.form["quantity"])
            limit = int(request.form.get("low_stock_limit", 5))

            if not name or price < 0 or qty < 0 or limit < 0:
                raise ValueError()

        except (KeyError, ValueError, InvalidOperation):
            flash("Enter valid product details.", "error")
            return render_template(
                "product_form.html", product=request.form, mode="Edit"
            )

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE products
SET product_name=%s, category=%s, price=%s,
    quantity=%s, low_stock_limit=%s
WHERE product_id=%s AND business_id=%s
            """, (
    name, category, price, qty, limit,
    pid, current_user.business_id
))
            conn.commit()
            flash("Product updated successfully.", "success")
        except Exception:
            conn.rollback()
            flash("Could not update product.", "error")
        finally:
            cur.close()
            conn.close()

        return redirect(url_for("products"))

    return render_template(
        "product_form.html", product=product, mode="Edit"
    )



# Delete product - Admin only
@app.route("/products/delete/<int:pid>", methods=["POST"])
@admin_required
def delete_product(pid):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Check sales history only within this business
        cur.execute(
            """
            SELECT COUNT(*)
            FROM sales
            WHERE product_id=%s AND business_id=%s
            """,
            (pid, current_user.business_id)
        )

        if cur.fetchone()[0]:
            flash("This product has sales history and cannot be deleted.", "error")
        else:
            # Delete only this business's product
            cur.execute(
                """
                DELETE FROM products
                WHERE product_id=%s AND business_id=%s
                """,
                (pid, current_user.business_id)
            )
            conn.commit()

            if cur.rowcount > 0:
                flash("Product deleted successfully.", "success")
            else:
                flash("Product not found.", "error")

    except Exception:
        conn.rollback()
        flash("Could not delete product.", "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("products"))



# Sales - Admin and Staff

@app.route("/sales", methods=["GET", "POST"])
@login_required
def sales():
    if request.method == "POST":
        try:
            pid = int(request.form["product_id"])
            qty = int(request.form["quantity_sold"])

            if pid < 1 or qty < 1:
                raise ValueError()

        except (KeyError, ValueError):
            flash("Choose a product and enter a quantity above zero.", "error")
            return redirect(url_for("sales"))

        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()

            # Find product belonging to the logged-in business
            cur.execute(
                """
                SELECT price, quantity
                FROM products
                WHERE product_id=%s AND business_id=%s
                FOR UPDATE
                """,
                (pid, current_user.business_id)
            )
            product = cur.fetchone()

            if not product:
                raise ValueError("Product not found.")

            if product["quantity"] < qty:
                raise ValueError(
                    f"Not enough stock. Available: {product['quantity']}."
                )

            total = Decimal(str(product["price"])) * qty

            # Update stock only for this business
            cur.execute(
                """
                UPDATE products
                SET quantity=quantity-%s
                WHERE product_id=%s AND business_id=%s
                """,
                (qty, pid, current_user.business_id)
            )

            # Save sale with business ID
            cur.execute("""
                INSERT INTO sales
                    (product_id, quantity_sold, total_amount, business_id)
                VALUES (%s, %s, %s, %s)
            """, (pid, qty, total, current_user.business_id))

            conn.commit()
            flash("Sale recorded and stock updated.", "success")

        except Exception as e:
            conn.rollback()
            flash(str(e), "error")
        finally:
            cur.close()
            conn.close()

        return redirect(url_for("sales"))

    # Show only this business's available products
    products_list = query_all("""
        SELECT product_id, product_name, price, quantity
        FROM products
        WHERE quantity > 0 AND business_id=%s
        ORDER BY product_name
    """, (current_user.business_id,))

    # Show only this business's sales history
    history = query_all("""
        SELECT s.sale_id, p.product_name, s.quantity_sold,
               s.total_amount, s.sale_date
        FROM sales s
        JOIN products p ON p.product_id = s.product_id
        WHERE s.business_id=%s
        ORDER BY s.sale_date DESC, s.sale_id DESC
        LIMIT 100
    """, (current_user.business_id,))

    return render_template(
        "sales.html", products=products_list, history=history
    )


# Reports - Admin only

@app.route("/reports")
@admin_required
def reports():
    today = date.today()

    # Today's sales summary for the logged-in business
    summary = query_one("""
        SELECT COALESCE(SUM(total_amount), 0) AS amount,
               COALESCE(SUM(quantity_sold), 0) AS units
        FROM sales
        WHERE DATE(sale_date)=%s
          AND business_id=%s
    """, (today, current_user.business_id))

    # Product-wise sales report for the logged-in business
    rows = query_all("""
        SELECT p.product_name, p.category, p.quantity,
               COALESCE(SUM(s.quantity_sold), 0) AS units_sold,
               COALESCE(SUM(s.total_amount), 0) AS revenue
        FROM products p
        LEFT JOIN sales s
            ON p.product_id = s.product_id
            AND s.business_id = %s
        WHERE p.business_id = %s
        GROUP BY p.product_id, p.product_name, p.category, p.quantity
        ORDER BY revenue DESC, p.product_name
    """, (current_user.business_id, current_user.business_id))

    return render_template(
        "reports.html", today=today, summary=summary, rows=rows
    )



# User management - Admin only

@app.route("/users")
@admin_required
def users():
    # Show only users belonging to the logged-in business
    user_list = query_all("""
        SELECT user_id, username, role, created_at
        FROM users
        WHERE business_id=%s
        ORDER BY user_id DESC
    """, (current_user.business_id,))

    return render_template("users.html", users=user_list)



@app.route("/users/add", methods=["GET", "POST"])
@admin_required
def add_user():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "staff")

        if len(username) < 3 or len(password) < 8:
            flash("Username must have 3 characters and password at least 8.", "error")
            return render_template("user_form.html")

        if role not in ("admin", "staff"):
            flash("Invalid user role.", "error")
            return render_template("user_form.html")

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO users
                    (username, password_hash, role, business_id)
                VALUES (%s, %s, %s, %s)
            """, (
                username,
                generate_password_hash(password),
                role,
                current_user.business_id
            ))

            conn.commit()
            flash("User account created successfully.", "success")
            return redirect(url_for("users"))

        except Exception:
            conn.rollback()
            flash("Could not create user. The username may already exist.", "error")
        finally:
            cur.close()
            conn.close()

    return render_template("user_form.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        business_name = request.form.get("business_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not business_name or len(username) < 3 or len(password) < 8:
            flash(
                "Enter a business name, username of at least 3 characters, "
                "and password of at least 8 characters.",
                "error"
            )
            return render_template("register.html")

        conn = get_connection()
        cur = conn.cursor()

        try:
            conn.start_transaction()

            # Create a new business
            cur.execute(
                "INSERT INTO businesses (business_name) VALUES (%s)",
                (business_name,)
            )
            business_id = cur.lastrowid

            # Create the business owner as Admin
            cur.execute("""
                INSERT INTO users
                    (username, password_hash, role, business_id)
                VALUES (%s, %s, %s, %s)
            """, (
                username,
                generate_password_hash(password),
                "admin",
                business_id
            ))

            conn.commit()
            flash("Business registered successfully. Please log in.", "success")
            return redirect(url_for("login"))

        except Exception:
            conn.rollback()
            flash(
                "Registration failed. The username may already exist.",
                "error"
            )
        finally:
            cur.close()
            conn.close()

    return render_template("register.html")


@app.route("/health")
def health():
    conn = get_connection()
    conn.close()
    return "Application and MySQL connection are working."


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
