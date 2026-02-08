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

# פונקציה לחילוץ נקודות בפורמט (x,y) מהקלט של המשתמש
def extract_user_points(text):
    # מחפש תבנית של (מספר,מספר)
    found = re.findall(r'\(\s*(-?\d*\.?\d+)\s*,\s*(-?\d*\.?\d+)\s*\)', text)
    return sorted([(float(x_val), float(y_val)) for x_val, y_val in found])

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        
        # הכנת פתרונות נקיים
        true_pts = sorted([format_num(p.evalf()) for p in true_domain])
        true_pts_str = ", ".join([str(p) for p in true_pts])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.info("נראה שזו לא התשובה הנכונה. אני ממליץ לך להסתכל ברמזים למטה ולנסות שוב.")
            except: pass

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            user_asymp = st.text_input("מהן משוואות האסימפטוטות האנכיות? (x = ?):", key="asymp_input")
            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (y = ?):", key="horiz_input")
            
            if user_asymp and user_horiz:
                st.success("מצוין! בוא נמשיך לנקודות חיתוך.")
                show_step_3 = True

        # --- שלב 3: נקודות חיתוך עם ציר x ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם ציר x")
            
            with st.expander("💡 רמז: איך מוצאים חיתוך עם ציר x?"):
                st.write("כדי למצוא חיתוך עם ציר $x$, עלינו להשוות את הפונקציה לאפס ($y=0$).")
                st.write("בפונקציית שבר, זה קורה כאשר ה**מונה** שווה לאפס.")
                st.write("**דוגמה:** עבור הפונקציה $f(x) = \\frac{x-5}{x+2}$:")
                st.latex(r"x-5 = 0 \implies x=5 \implies (5,0)")
                st.info("זכור: התשובה צריכה להיות בפורמט של נקודה: **(x,y)**. אם אין חיתוך, כתוב 'אין'.")

            user_x_input = st.text_input("הזן את נקודות החיתוך עם ציר x (למשל: (2,0) ):", key="x_intercept_input")
            
            # חישוב תשובה נכונה
            x_roots = sp.solve(num, x)
            # סינון שורשים שלא בתחום ההגדרה
            valid_x_roots = [r for r in x_roots if r not in true_domain]
            true_x_points = sorted([(float(r.evalf()), 0.0) for r in valid_x_roots])

            show_final_plot = False
            if user_x_input:
                try:
                    if user_x_input.lower() == "אין":
                        is_correct = (len(true_x_points) == 0)
                    else:
                        user_points = extract_user_points(user_x_input)
                        is_correct = (len(user_points) == len(true_x_points)) and \
                                     all(np.allclose(user_points[i], true_x_points[i]) for i in range(len(user_points)))
                    
                    if is_correct:
                        st.success("מעולה! מצאת את נקודות החיתוך עם ציר x.")
                        show_final_plot = True
                    else:
                        st.info("לא זאת לא התשובה הנכונה, אני ממליץ לך לקרוא את הרמז ולנסות שוב ואם אינך רוצה לנסות שוב לחץ על הצג פיתרון ושרטט")
                except:
                    st.warning("נא להקפיד על פורמט הנקודה: (מספר,מספר)")

            if st.button("הצג פיתרון ושרטט"):
                show_final_plot = True

            if show_final_plot:
                # הצגת התשובה המילולית
                if not true_x_points:
                    st.write("אין נקודות חיתוך עם ציר x.")
                else:
                    points_str = ", ".join([f"({format_num(p[0])}, 0)" for p in true_x_points])
                    st.write(f"נקודות החיתוך הן: **{points_str}**")

                # שרטוט הגרף עם הנקודות
                fig = go.Figure()
                # הוספת הנקודות לגרף
                for p in true_x_points:
                    fig.add_trace(go.Scatter(
                        x=[p[0]], y=[0], 
                        mode='markers+text',
                        marker=dict(color='green', size=12),
                        text=[f"({format_num(p[0])},0)"],
                        textposition="bottom center",
                        name="חיתוך x"
                    ))
                
                fig.update_xaxes(zeroline=True, zerolinewidth=2, range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=2, range=[-10, 10])
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig)

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
