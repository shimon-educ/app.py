import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("חקירה מודרכת עם פתרון מלא")

def format_num(n):
    try:
        n_float = float(n)
        return int(n_float) if n_float.is_integer() else round(n_float, 2)
    except: return n

input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])

        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        user_domain = st.text_input("מהם הערכים שמאפסים את המכנה? (למשל: 5, 2-)")
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("מעולה! מצאת את נקודות אי-ההגדרה.")
                    st.session_state['step1_done'] = True
                else:
                    st.error("לא בדיוק... נסה להיעזר ברמזים או בפתרון המלא.")
            except: st.warning("נא להזין מספרים מפרדים בפסיק.")

        # --- בלוק הפתרון המפורט ---
        with st.expander("זקוק לפתרון מלא של המשוואה הריבועית?"):
            st.write("נפתור את המשוואה: " + f"${sp.latex(den)} = 0$")
            
            # חילוץ מקדמים אוטומטי
            a = sp.Poly(den, x).coeffs()[0] if len(sp.Poly(den, x).coeffs()) > 2 else 0
            b = sp.Poly(den, x).coeffs()[1] if len(sp.Poly(den, x).coeffs()) > 2 else sp.Poly(den, x).coeffs()[0]
            c = sp.Poly(den, x).coeffs()[2] if len(sp.Poly(den, x).coeffs()) > 2 else sp.Poly(den, x).coeffs()[1]
            
            st.write(f"המקדמים שלנו הם: $a={a}, b={b}, c={c}$")
            st.write("נציב בנוסחת השורשים:")
            st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
            
            discriminant = b**2 - 4*a*c
            st.latex(f"x_{{1,2}} = \\frac{{-({b}) \\pm \\sqrt{{{b}^2 - 4 \\cdot {a} \\cdot {c}}}}}{{2 \\cdot {a}}}")
            st.latex(f"x_{{1,2}} = \\frac{{{-b} \\pm \\sqrt{{{discriminant}}}}}{{{2*a}}}")
            
            st.info(f"הפתרונות הם: {true_pts_str}")
            if st.button("הבנתי, המשך לחקירה"):
                st.session_state['step1_done'] = True

        if st.session_state.get('step1_done'):
            st.markdown("---")
            st.header("שלב 2: הגרף והנגזרת")
            
            # גרף
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-10, 10, 1000)
            y_vals = f_num(x_vals)
            y_vals[np.abs(y_vals) > 20] = np.nan
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)"))
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
            st.plotly_chart(fig)
            
            if st.checkbox("הצג נגזרת סופית"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("וודא שהפונקציה נכתבה נכון (למשל x**2 למקדם ריבועי).")

if st.sidebar.button("אפס הכל"):
    st.session_state.clear()
    st.rerun()
