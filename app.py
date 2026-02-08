import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

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

        # שלב 1: תחום הגדרה
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        user_domain = st.text_input("מהם הערכים שמאפסים את המכנה? (למשל: 5, 2-)")
        
        show_full_solution = False
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("מעולה! מצאת את נקודות אי-ההגדרה.")
                    st.session_state['step1_done'] = True
                else:
                    st.error("לא בדיוק... נסה להיעזר ברמזים.")
            except: st.warning("נא להזין מספרים מופרדים בפסיק.")

        # --- מערכת רמזים הדרגתית ---
        if not st.session_state.get('step1_done'):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                hint1 = st.checkbox("רמז 1: המשוואה")
            with col2:
                hint2 = st.checkbox("רמז 2: פירוק לגורמים")
            with col3:
                give_up = st.button("התייאשתי, הצג פתרון")

            if hint1:
                st.info("עליך לפתור את המשוואה שמתקבלת מהמכנה:")
                st.latex(sp.latex(den) + "= 0")
            
            if hint2:
                st.info("אפשר לפרק את המכנה לגורמים (טרינום או גורם משותף):")
                st.latex(sp.latex(sp.factor(den)) + "= 0")

            if give_up:
                st.session_state['show_full_solution'] = True

        # --- הצגת הפתרון המלא עם נוסחת השורשים ---
        if st.session_state.get('show_full_solution'):
            st.markdown("---")
            st.subheader("💡 פתרון מלא באמצעות נוסחת השורשים")
            
            # חילוץ מקדמים
            try:
                poly_den = sp.Poly(den, x)
                a = format_num(poly_den.coeff_inst(x, 2)) if poly_den.degree() >= 2 else 0
                b = format_num(poly_den.coeff_inst(x, 1))
                c = format_num(poly_den.coeff_inst(x, 0))
                
                st.write(f"עבור המכנה ${sp.latex(den)}$, המקדמים הם: $a={a}, b={b}, c={c}$")
                st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                
                disc = b**2 - 4*a*c
                st.latex(f"x_{{1,2}} = \\frac{{-({b}) \\pm \\sqrt{{{b}^2 - 4 \\cdot {a} \\cdot {c}}}}}{{2 \\cdot {a}}}")
                st.latex(f"x_{{1,2}} = \\frac{{{-b} \\pm \\sqrt{{{disc}}}}}{{{2*a}}}")
                
                st.write(f"הערכים המאפסים הם: **{true_pts_str}**")
                if st.button("הבנתי, בוא נמשיך לגרף"):
                    st.session_state['step1_done'] = True
                    st.session_state['show_full_solution'] = False
                    st.rerun()
            except:
                st.write(f"הערכים המאפסים הם: **{true_pts_str}**")
                if st.button("המשך לחקירה"):
                    st.session_state['step1_done'] = True
                    st.rerun()

        # --- שלב 2: הצגת התוצאות ---
        if st.session_state.get('step1_done'):
            st.markdown("---")
            st.header("שלב 2: הצגה גרפית ונגזרת")
            
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-10, 10, 1000)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_vals = f_num(x_vals)
            y_vals[np.abs(y_vals) > 20] = np.nan
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)", line=dict(color='blue')))
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
            
            st.plotly_chart(fig)
            
            if st.checkbox("הצג נגזרת סופית לבדיקה"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("אפס חקירה"):
    st.session_state.clear()
    st.rerun()
