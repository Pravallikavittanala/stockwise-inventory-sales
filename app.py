import os
from decimal import Decimal, InvalidOperation
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

def query_all(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def query_one(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

@app.route("/")
def dashboard():
    stats = query_one("""
      SELECT (SELECT COUNT(*) FROM products) total_products,
             (SELECT COALESCE(SUM(quantity),0) FROM products) total_stock,
             (SELECT COUNT(*) FROM products WHERE quantity <= low_stock_limit) low_stock,
             (SELECT COALESCE(SUM(total_amount),0) FROM sales) total_sales
    """)
    recent = query_all("""SELECT s.sale_id,p.product_name,s.quantity_sold,s.total_amount,s.sale_date
                          FROM sales s JOIN products p ON p.product_id=s.product_id
                          ORDER BY s.sale_date DESC,s.sale_id DESC LIMIT 6""")
    low = query_all("""SELECT product_name,quantity,low_stock_limit FROM products
                       WHERE quantity <= low_stock_limit ORDER BY quantity LIMIT 5""")
    return render_template("dashboard.html", stats=stats, recent=recent, low=low)

@app.route("/products")
def products():
    q = request.args.get("q","").strip()
    if q:
        items = query_all("SELECT * FROM products WHERE product_name LIKE %s OR category LIKE %s ORDER BY product_id DESC",
                          (f"%{q}%",f"%{q}%"))
    else:
        items = query_all("SELECT * FROM products ORDER BY product_id DESC")
    return render_template("products.html", products=items, q=q)

@app.route("/products/add", methods=["GET","POST"])
def add_product():
    if request.method == "POST":
        try:
            name = request.form["product_name"].strip()
            category = request.form.get("category","").strip()
            price = Decimal(request.form["price"])
            qty = int(request.form["quantity"])
            limit = int(request.form.get("low_stock_limit",5))
            if not name or price < 0 or qty < 0 or limit < 0: raise ValueError()
        except (KeyError,ValueError,InvalidOperation):
            flash("Enter a name and valid non-negative price and quantities.","error")
            return render_template("product_form.html", product=request.form, mode="Add")
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO products(product_name,category,price,quantity,low_stock_limit) VALUES(%s,%s,%s,%s,%s)",
                        (name,category,price,qty,limit))
            conn.commit()
            flash("Product added successfully.","success")
        except Exception as e:
            conn.rollback(); flash(f"Could not add product: {e}","error")
        finally:
            cur.close(); conn.close()
        return redirect(url_for("products"))
    return render_template("product_form.html", product={}, mode="Add")

@app.route("/products/edit/<int:pid>", methods=["GET","POST"])
def edit_product(pid):
    product = query_one("SELECT * FROM products WHERE product_id=%s",(pid,))
    if not product:
        flash("Product not found.","error"); return redirect(url_for("products"))
    if request.method == "POST":
        try:
            name=request.form["product_name"].strip()
            category=request.form.get("category","").strip()
            price=Decimal(request.form["price"]); qty=int(request.form["quantity"])
            limit=int(request.form.get("low_stock_limit",5))
            if not name or price < 0 or qty < 0 or limit < 0: raise ValueError()
        except (KeyError,ValueError,InvalidOperation):
            flash("Enter valid product details.","error")
            return render_template("product_form.html",product=request.form,mode="Edit")
        conn=get_connection()
        try:
            cur=conn.cursor()
            cur.execute("""UPDATE products SET product_name=%s,category=%s,price=%s,quantity=%s,low_stock_limit=%s
                           WHERE product_id=%s""",(name,category,price,qty,limit,pid))
            conn.commit(); flash("Product updated.","success")
        except Exception as e:
            conn.rollback(); flash(f"Could not update product: {e}","error")
        finally:
            cur.close(); conn.close()
        return redirect(url_for("products"))
    return render_template("product_form.html",product=product,mode="Edit")

@app.route("/products/delete/<int:pid>",methods=["POST"])
def delete_product(pid):
    conn=get_connection()
    try:
        cur=conn.cursor()
        cur.execute("SELECT COUNT(*) FROM sales WHERE product_id=%s",(pid,))
        if cur.fetchone()[0]:
            flash("This product has sales history and cannot be deleted.","error")
        else:
            cur.execute("DELETE FROM products WHERE product_id=%s",(pid,))
            conn.commit(); flash("Product deleted.","success")
    except Exception as e:
        conn.rollback(); flash(f"Could not delete product: {e}","error")
    finally:
        cur.close(); conn.close()
    return redirect(url_for("products"))

@app.route("/sales",methods=["GET","POST"])
def sales():
    if request.method=="POST":
        try:
            pid=int(request.form["product_id"]); qty=int(request.form["quantity_sold"])
            if pid < 1 or qty < 1: raise ValueError()
        except (KeyError,ValueError):
            flash("Choose a product and enter a quantity above zero.","error")
            return redirect(url_for("sales"))
        conn=get_connection()
        try:
            cur=conn.cursor(dictionary=True)
            conn.start_transaction()
            cur.execute("SELECT price,quantity FROM products WHERE product_id=%s FOR UPDATE",(pid,))
            p=cur.fetchone()
            if not p: raise ValueError("Product not found.")
            if p["quantity"] < qty: raise ValueError(f"Not enough stock. Available: {p['quantity']}.")
            total=Decimal(str(p["price"]))*qty
            cur.execute("UPDATE products SET quantity=quantity-%s WHERE product_id=%s",(qty,pid))
            cur.execute("INSERT INTO sales(product_id,quantity_sold,total_amount) VALUES(%s,%s,%s)",(pid,qty,total))
            conn.commit(); flash("Sale recorded and stock updated.","success")
        except Exception as e:
            conn.rollback(); flash(str(e),"error")
        finally:
            cur.close(); conn.close()
        return redirect(url_for("sales"))
    products= query_all("SELECT product_id,product_name,price,quantity FROM products WHERE quantity>0 ORDER BY product_name")
    history=query_all("""SELECT s.sale_id,p.product_name,s.quantity_sold,s.total_amount,s.sale_date
                         FROM sales s JOIN products p ON p.product_id=s.product_id
                         ORDER BY s.sale_date DESC,s.sale_id DESC LIMIT 100""")
    return render_template("sales.html",products=products,history=history)

@app.route("/reports")
def reports():
    today=date.today()
    summary=query_one("""SELECT COALESCE(SUM(total_amount),0) amount,COALESCE(SUM(quantity_sold),0) units
                         FROM sales WHERE DATE(sale_date)=%s""",(today,))
    rows=query_all("""SELECT p.product_name,p.category,p.quantity,
                      COALESCE(SUM(s.quantity_sold),0) units_sold,
                      COALESCE(SUM(s.total_amount),0) revenue
                      FROM products p LEFT JOIN sales s ON p.product_id=s.product_id
                      GROUP BY p.product_id,p.product_name,p.category,p.quantity
                      ORDER BY revenue DESC,p.product_name""")
    return render_template("reports.html",today=today,summary=summary,rows=rows)

@app.route("/health")
def health():
    conn=get_connection(); conn.close()
    return "Application and MySQL connection are working."

if __name__=="__main__":
    app.run(debug=True)
