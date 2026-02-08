import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# הגדרות שפה וכותרת
st.set_page_config(page_title="MathBuddy - חוקר הפונקציות", layout="wide")
st.title("📊 MathBuddy: חוקר פונקציות רציונליות")
st.markdown("---")

# הזנת פונקציה מהתלמיד
input_func = st.text_input("הכנס את הפונקציה שלך (למשל: x**2 / (x-1)):", "x**2 / (x-1)")

if input_func:
    try:
        x = sp.symbols('x')
        # המרה של הביטוי למתמטיקה
        f = sp.sympify(input_func)
        
        # חישובים מאחורי הקלעים
        num, den = sp.fraction(f)
        domain = sp.solve(den, x)
        f_prime = sp.diff(f, x)
        critical_pts = sp.solve(f_prime, x)
        h_asymptote = sp.limit(f, x, sp.oo)

        # תצוגה לתלמיד בטאבים (שלבים)
        tab1, tab2, tab3 = st.tabs(["🔍 שלבי החקירה", "📈 הגרף שלי", "💡 עזרה בחישוב"])

        with tab1:
            st.subheader("ניתוח הפונקציה:")
            st.write(f"**1. תחום הגדרה:** הפונקציה לא מוגדרת כאשר המכנה מתאפס, כלומר: $x = {domain}$")
            
            if h_asymptote.is_number:
                st.write(f"**2. אסימפטוטה אופקית:** הפונקציה שואפת לערך $y = {h_asymptote}$ באינסוף.")
            else:
                st.write("**2. אסימפטוטה אופקית:** אין אסימפטוטה אופקית (הפונקציה שואפת לאינסוף).")
            
            st.write(f"**3. נקודות חשודות כקיצון:** אלו הערכים שמאפסים את הנגזרת: $x = {critical_pts}$")
            
        with tab2:
            # יצירת גרף אינטראקטיבי
            f_num = sp.lambdify(x, f, "numpy")
            x_range = np.linspace(-10, 10, 1000)
            y_range = f_num(x_range)
            
            # ניקוי קפיצות ליד אסימפטוטות
            y_range[np.abs(y_range) > 30] = np.nan 

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_range, y=y_range, name="f(x)", line=dict(color='blue', width=3)))
            
            # הוספת אסימפטוטות אנכיות (אדום)
            for pt in domain:
                try:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
                except: continue
            
            # הוספת אסימפטוטה אופקית (ירוק)
            if h_asymptote.is_number:
                fig.add_hline(y=float(h_asymptote), line_dash="dash", line_color="green")

            fig.update_layout(title="ייצוג גרפי של החקירה", xaxis_title="x", yaxis_title="f(x)", height=600)
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.info("כך גזרתי את הפונקציה:")
            st.latex(r"f'(x) = " + sp.latex(f_prime))
            st.write("זכור להשתמש בנוסחת נגזרת המנה!")

    except Exception as e:
        st.error("שגיאה בפענוח הפונקציה. וודא שהשתמשת ב- * לכפל וב- ** לחזקה (למשל x בריבוע זה x**2).")
