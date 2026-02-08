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

# פונקציה לפירוש קלט של נקודות בפורמט (x,y)
def extract_points(user_input):
    points = re.findall(r'\(\s*(-?\d*\.?\d+)\s*,\s*(-?\d*\.?\d+)\s*\)', user_input)
    return sorted([(float(x_val), float(y_val)) for x_val, y_val in points])

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
        
        # שלב 1 ו-2 (מקוצר לצורך התצוגה, נשאר כפי שהיה בקוד הקודם)
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        user_domain = st.text_input("הזן ערכים שמאפסים מכנה:", key="d_in")
        
        show_step_3 = False
        if user_domain:
            # לוגיקת מעבר (בדומה לקוד הקודם שלך)
            show_step_3 = True 

        # --- שלב 3: חיתוך עם ציר x ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם הצירים")
            st.subheader("חיתוך עם ציר x")

            with st.expander("💡 רמז: איך כותבים נקודת חיתוך עם ציר x?"):
                st.write("בנקודת חיתוך עם ציר x, ה-y הוא תמיד 0.")
                st.write("לכן, הפורמט חייב להיות: **(x, 0)**.")
                st.write("**דוגמה:** אם המונה מתאפס ב- $x=3$, נכתוב: `(3,0)`.")
                st.info("אם יש כמה נקודות, רשום אותן זו אחר זו. למשל: `(3,0), (-1,0)`")

            user_x_input = st.text_input("מהן נקודות החיתוך עם ציר x? (כתוב בפורמט: (x,y)):", key="x_point_input")

            # חישוב תשובה נכונה
            x_roots = sp.solve(num, x)
            valid_x_roots = [p for p in x_roots if p not in true_domain]
            true_x_points = sorted([(float(p.evalf()), 0.0) for p in valid_x_roots])

            show_final = False
            if user_x_input:
                try:
                    if user_x_input.lower() == "אין":
                        correct_x = (len(true_x_points) == 0)
                    else:
                        user_pts = extract_points(user_x_input)
                        correct_x = (len(user_pts) == len(true_x_points)) and \
                                    all(np.allclose(user_pts[i], true_x_points[i]) for i in range(len(user_pts)))

                    if correct_x:
                        st.success(f"מצוין! הנקודות הן: {', '.join([f'({format_num(p[0])},0)' for p in true_x_points]) if true_x_points else 'אין'}")
                        show_final = True
                    else:
                        st.info("לא, זאת לא התשובה הנכונה. ודא שהשתמשת בפורמט (x,y), אני ממליץ לך לקרוא את הרמז ולנסות שוב ואם אינך רוצה לנסות שוב לחץ על הצג פיתרון ושרטט.")
                except:
                    st.warning("נא להקפיד על פורמט הנקודה: (מספר, מספר)")

            if st.button("הצג פיתרון ושרטט"):
                show_final = True

            if show_final:
                # שרטוט הגרף (כפי שהופיע בקוד הקודם)
                fig = go.Figure()
                for p in true_x_points:
                    fig.add_trace(go.Scatter(x=[p[0]], y=[0], mode='markers+text', 
                                             text=[f"({format_num(p[0])},0)"], textposition="bottom center",
                                             marker=dict(color='green', size=12)))
                fig.update_xaxes(zeroline=True, range=[-10, 10])
                fig.update_yaxes(zeroline=True, range=[-10, 10])
                st.plotly_chart(fig)

    except:
        st.error("שגיאה בביטוי")
