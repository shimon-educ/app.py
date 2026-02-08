import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("כאן לומדים לחקור פונקציות צעד אחר צעד.")

def format_num(n):
    try:
        n_float = float(n)
        return int(n_float) if n_float.is_integer() else round(n_float, 2)
    except:
        return n

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        
        # חישוב נתונים מתמטיים מראש
        true_domain = sp.solve(den, x)
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        horiz_asy = sp.limit(f, x, sp.oo)
        horiz_val = format_num(horiz_asy.evalf())

        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        with st.expander("🤔 איך מוצאים תחום הגדרה? (הסבר תיאורטי)"):
            st.write("כדי למצוא תחום הגדרה של שבר, נחפש מתי המכנה מתאפס ($המכנה = 0$). אלו הנקודות שהפונקציה לא מוגדרת בהן.")
        
        user_domain = st.text_input("מהם הערכים שמאפסים את המכנה? (הפרד בפסיקים):", key="domain_input")
        
        step_1_passed = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("נכון מאוד!")
                    step_1_passed = True
            except: st.warning("נא להזין מספרים מופרדים בפסיק.")

        if not step_1_passed:
            if st.button("התייאשתי, הצג פתרון שורשים"):
                st.info("מהלך הפתרון:")
                try:
                    p_poly = sp.Poly(den, x)
                    coeffs = p_poly.all_coeffs()
                    if len(coeffs) == 3:
                        a, b, c = [format_num(v) for v in coeffs]
                        st.latex(f"x_{{1,2}} = \\frac{{-({b}) \\pm \\sqrt{{{b}^2 - 4 \cdot {a} \cdot {c}}}}}{{2 \cdot {a}}}")
                except: pass
                st.session_state['force_s1'] = True
        
        if st.session
