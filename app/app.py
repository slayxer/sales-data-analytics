from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "salesiq_secret"

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sales.csv")

def get_df():
    df = pd.read_csv(CSV_PATH)
    df['revenue'] = df['quantity'] * df['price']
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%b %Y')
    return df

# ─── Dashboard ───────────────────────────────────────────────
@app.route("/")
def home():
    try:
        df = get_df()
        total_revenue = int(df['revenue'].sum())
        total_orders = len(df)
        top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).to_dict()
        city_sales = df.groupby('city')['revenue'].sum().sort_values(ascending=False).to_dict()
        return render_template("index.html",
            revenue=total_revenue, orders=total_orders,
            products=top_products, cities=city_sales)
    except Exception as e:
        return error_page(e)

# ─── Products ────────────────────────────────────────────────
@app.route("/products")
def products():
    try:
        df = get_df()
        selected = request.args.get('product', 'All')
        all_products = sorted(df['product'].unique().tolist())

        if selected != 'All':
            df = df[df['product'] == selected]

        product_summary = (
            df.groupby('product')
            .agg(total_revenue=('revenue','sum'), total_orders=('order_id','count'), total_qty=('quantity','sum'))
            .reset_index()
            .sort_values('total_revenue', ascending=False)
        )

        monthly_trend = df.groupby(['month','product'])['revenue'].sum().reset_index()
        months_sorted = sorted(df['date'].dt.to_period('M').unique())
        months_str = [str(m) for m in months_sorted]
        months_label = [pd.Period(m, freq='M').strftime('%b %Y') for m in months_str]

        trend_data = {}
        for p in (all_products if selected == 'All' else [selected]):
            trend_data[p] = []
            for m in months_str:
                label = pd.Period(m, freq='M').strftime('%b %Y')
                val = monthly_trend[
                    (monthly_trend['month'] == label) & (monthly_trend['product'] == p)
                ]['revenue'].sum()
                trend_data[p].append(int(val))

        return render_template("products.html",
            summary=product_summary.to_dict(orient='records'),
            all_products=all_products,
            selected=selected,
            trend_data=trend_data,
            months=months_label)
    except Exception as e:
        return error_page(e)

# ─── Cities ──────────────────────────────────────────────────
@app.route("/cities")
def cities():
    try:
        df = get_df()
        selected = request.args.get('city', 'All')
        all_cities = sorted(df['city'].unique().tolist())

        if selected != 'All':
            df = df[df['city'] == selected]

        city_summary = (
            df.groupby('city')
            .agg(total_revenue=('revenue','sum'), total_orders=('order_id','count'))
            .reset_index()
            .sort_values('total_revenue', ascending=False)
        )

        city_product = df.groupby(['city','product'])['revenue'].sum().reset_index()
        city_product_dict = {}
        for city in (all_cities if selected == 'All' else [selected]):
            sub = city_product[city_product['city'] == city]
            city_product_dict[city] = sub.set_index('product')['revenue'].to_dict()

        return render_template("cities.html",
            summary=city_summary.to_dict(orient='records'),
            all_cities=all_cities,
            selected=selected,
            city_product=city_product_dict)
    except Exception as e:
        return error_page(e)

# ─── Reports ─────────────────────────────────────────────────
@app.route("/reports")
def reports():
    try:
        df = get_df()

        monthly = df.groupby('month').agg(revenue=('revenue','sum'), orders=('order_id','count')).reset_index()
        monthly['month_dt'] = pd.to_datetime(monthly['month'], format='%b %Y')
        monthly = monthly.sort_values('month_dt')

        best_month = monthly.loc[monthly['revenue'].idxmax(), 'month']
        best_product = df.groupby('product')['revenue'].sum().idxmax()
        best_city = df.groupby('city')['revenue'].sum().idxmax()
        avg_order_value = int(df['revenue'].sum() / len(df))

        return render_template("reports.html",
            monthly=monthly.to_dict(orient='records'),
            best_month=best_month,
            best_product=best_product,
            best_city=best_city,
            avg_order_value=avg_order_value,
            total_revenue=int(df['revenue'].sum()),
            total_orders=len(df))
    except Exception as e:
        return error_page(e)

# ─── Data Entry ──────────────────────────────────────────────
@app.route("/entry", methods=["GET", "POST"])
def entry():
    try:
        df = get_df()
        all_products = sorted(df['product'].unique().tolist())
        all_cities = sorted(df['city'].unique().tolist())

        if request.method == "POST":
            product  = request.form.get("product").strip()
            quantity = int(request.form.get("quantity"))
            price    = float(request.form.get("price"))
            city     = request.form.get("city").strip()
            date     = request.form.get("date")

            # Get next order_id
            raw_df = pd.read_csv(CSV_PATH)
            next_id = int(raw_df['order_id'].max()) + 1

            new_row = pd.DataFrame([{
                "order_id": next_id,
                "product": product,
                "quantity": quantity,
                "price": price,
                "city": city,
                "date": date
            }])

            updated_df = pd.concat([raw_df, new_row], ignore_index=True)
            updated_df.to_csv(CSV_PATH, index=False)

            flash(f"✅ Order #{next_id} added successfully!", "success")
            return redirect(url_for('entry'))

        # Recent 10 entries for preview
        recent = df.sort_values('date', ascending=False).head(10)
        recent_records = recent[['order_id','product','quantity','price','city','date','revenue']].to_dict(orient='records')

        return render_template("entry.html",
            all_products=all_products,
            all_cities=all_cities,
            recent=recent_records,
            today=datetime.today().strftime('%Y-%m-%d'))
    except Exception as e:
        return error_page(e)

def error_page(e):
    return f"""
    <html><body style="font-family:Arial;margin:40px;">
    <h2 style="color:red;">❌ Error</h2>
    <p style="background:#fee;padding:10px;border-radius:8px;"><strong>{e}</strong></p>
    </body></html>
    """

if __name__ == "__main__":
    app.run(debug=True)