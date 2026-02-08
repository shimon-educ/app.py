import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import re

# הגדרות עמוד
st.set_page_config(page_title="MathBuddy", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

# פונקציית עזר לעיצוב מספרים
def format_num(n):
    try:
        n_float = float(n)
        return int(n_float) if n_float.is_integer() else round(n_float, 2)
    except:
        return n

# פונקציה לחילוץ נקודות בפורמט (x,y)
def extract_points(text):
    found = re.findall(r'\(\s*(-?\d*\.?\d+)\s*,\s*(-?\d*\.?\d+)\s*\)', text)
    return sorted([(float(x), float(y)) for x, y in found])

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        if user_domain:
            try:
                u_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(u_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.info("נראה שזו לא התשובה הנכונה. אני ממליץ לך להסתכל ברמזים למטה ולנסות שוב.")
            except: pass

        if st.session_state.get('force_step_2'): show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            user_asymp = st.text_input("אסימפטוטות אנכיות (x = ?):", key="asymp_input")
            user_horiz = st.text_input("אסימפטוטה אופקית (y = ?):", key="horiz_input")
            
            if user_asymp and user_horiz:
                st.success("מצוין! בוא נמשיך.")
                show_step_3 = True

        # --- שלב 3: חיתוך עם ציר x ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: חיתוך עם ציר x")
            
            with st.expander("💡 רמז: איך מוצאים חיתוך עם ציר x?"):
                st.write("מתי הפונקציה פוגשת את ציר $x$? כשערך ה-$y$ הוא 0.")
                st.write("בפונקציית שבר, זה קורה כשה**מונה** שווה ל-0.")
                st.write("**פורמט התשובה:** כתוב את הנקודה כך: `(x,0)`.")

            user_x_input = st.text_input("מהן נקודות החיתוך עם ציר x? (למשל: (0,0) ):", key="x_int_input")
            
            # חישוב תשובה נכונה
            x_roots = [r for r in sp.solve(num, x) if r not in true_domain]
            true_x_points = sorted([(float(r.evalf()), 0.0) for r in x_roots])

            if user_x_input:
                try:
                    if user_x_input.lower() == "אין":
                        correct = (len(true_x_points) == 0)
                    else:
                        u_points = extract_points(user_x_input)
                        correct = (len(u_points) == len(true_x_points)) and \
                                  all(np.allclose(u_points[i], true_x_points[i]) for i in range(len(u_points)))
                    
                    if correct:
                        st.success("מצוין! מצאת את נקודות החיתוך.")
                    else:
                        st.info("לא זאת לא התשובה הנכונה, אני ממליץ לך לקרוא את הרמז ולנסות שוב ואם אינך רוצה לנסות שוב לחץ על הצג פיתרון ושרטט")
                except: st.warning("הזן בפורמט: (x,y)")

            if st.button("הצג פיתרון ושרטט"):
                st.write(f"הנקודות הן: {[(format_num(p[0]), 0) for p in true_x_points]}")
                fig = go.Figure()
                for p in true_x_points:
                    fig.add_trace(go.Scatter(x=[p[0]], y=[0], mode='markers+text', text=[f"({format_num(p[0])},0)"], textposition="bottom center", marker=dict(color='green', size=12)))
                fig.update_xaxes(zeroline=True, range=[-10, 10])
                fig.update_yaxes(zeroline=True, range=[-10, 10])
                st.plotly_chart(fig)

    except: st.error("ביטוי לא תקין")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
