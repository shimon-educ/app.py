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

# פונקציה לחילוץ נקודות בפורמט (x,y) מקלט טקסטואלי
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
                user_pts_list = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts_list, [float(p) for p in true_pts]):
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
                # כאן אפשר להוסיף בדיקה לוגית דומה לשלב 1, לצורך הדוגמה נניח שזה מוביל לשלב 3
                show_step_3 = True

        # --- שלב 3: נקודות חיתוך עם הצירים ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם הצירים")
            
            # --- חיתוך עם ציר X ---
            st.subheader("1. חיתוך עם ציר x")
            with st.expander("💡 איך מוצאים חיתוך עם ציר x?"):
                st.write("בנקודת החיתוך עם ציר $x$, גובה הפונקציה הוא אפס ($y=0$).")
                st.write("לכן, עלינו להשוות את המונה לאפס: $num(x) = 0$.")
                st.write("**דוגמה:** עבור $f(x) = \\frac{x-2}{x+1}$, נפתור $x-2=0$ ונקבל $x=2$.")
                st.info("את התשובה יש לכתוב כנקודה: **(2,0)**. אם יש כמה נקודות, הפרד אותן בפסיק.")

            user_x_int = st.text_input("הזן נקודות חיתוך עם ציר x (בפורמט (x,y)):", key="x_intercept_input")
            
            # --- חיתוך עם ציר Y ---
            st.subheader("2. חיתוך עם ציר y")
            with st.expander("💡 איך מוצאים חיתוך עם ציר y?"):
                st.write("בנקודת החיתוך עם ציר $y$, ערך ה-$x$ הוא אפס.")
                st.write("נציב $x=0$ בפונקציה ונחשב את $f(0)$.")
                st.write("**דוגמה:** עבור $f(x) = \\frac{x+6}{x-2}$, נציב $0$ ונקבל $\\frac{6}{-2} = -3$.")
                st.info("את התשובה יש לכתוב כנקודה: **(0,-3)**.")

            user_y_int = st.text_input("הזן נקודת חיתוך עם ציר y (בפורמט (x,y)):", key="y_intercept_input")

            # לוגיקת בדיקה לחיתוך x
            true_x_roots = [r for r in sp.solve(num, x) if r not in true_domain]
            true_x_points = sorted([(float(r.evalf()), 0.0) for r in true_x_roots])
            
            # לוגיקת בדיקה לחיתוך y
            try:
                if 0 in true_domain:
                    true_y_point = [] # אין חיתוך כי x=0 מחוץ לתחום
                else:
                    true_y_val = f.subs(x, 0)
                    true_y_point = [(0.0, float(true_y_val.evalf()))]
            except: true_y_point = []

            if user_x_int and user_y_int:
                try:
                    u_x_pts = extract_points(user_x_int)
                    u_y_pts = extract_points(user_y_int)
                    
                    correct_x = (len(u_x_pts) == len(true_x_points)) and all(np.allclose(u_x_pts[i], true_x_points[i]) for i in range(len(u_x_pts)))
                    correct_y = (len(u_y_pts) == len(true_y_point)) and all(np.allclose(u_y_pts[i], true_y_point[i]) for i in range(len(u_y_pts)))

                    if correct_x and correct_y:
                        st.success("מעולה! מצאת את כל נקודות החיתוך.")
                    else:
                        st.info("לא זאת לא התשובה הנכונה, אני ממליץ לך לקרוא את הרמז ולנסות שוב ואם אינך רוצה לנסות שוב לחץ על הצג פיתרון ושרטט.")
                except:
                    st.warning("נא להזין נקודות בפורמט תקין: (x,y)")

            if st.button("הצג פיתרון ושרטט"):
                # שרטוט הגרף עם הנקודות
                fig = go.Figure()
                # הוספת נקודות חיתוך x בירוק
                for p in true_x_points:
                    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode='markers+text', 
                                             text=[f"({format_num(p[0])},0)"], textposition="top center",
                                             marker=dict(color='green', size=10), name="חיתוך x"))
                # הוספת נקודת חיתוך y בכתום
                for p in true_y_point:
                    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode='markers+text', 
                                             text=[f"(0,{format_num(p[1])})"], textposition="middle right",
                                             marker=dict(color='orange', size=10), name="חיתוך y"))
                
                fig.update_xaxes(zeroline=True, zerolinewidth=2, range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=2, range=[-10, 10])
                fig.update_layout(height=500, title="נקודות חיתוך על הצירים")
                st.plotly_chart(fig)

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
