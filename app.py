import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy - מעבדת החקירה", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("כאן לומדים לחקור צעד אחר צעד!")

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        # הפיכת הפתרונות למספרים פשוטים להשוואה
        true_pts = sorted([float(p.evalf()) for p in true_domain])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.write(f"הפונקציה היא: ${sp.latex(f)}$")
        st.write("כדי למצוא את תחום ההגדרה, עלינו למצוא מה מאפס את המכנה.")
        
        user_domain = st.text_input("מהם הערכים שמאפסים את המכנה? (למשל: 1, -3)")
        
        show_step_2 = False
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, true_pts):
                    st.success("מעולה! מצאת את נקודות אי-ההגדרה.")
                    show_step_2 = True
                else:
                    st.error("לא בדיוק... נסה לבדוק שוב את פירוק המכנה.")
                    if st.button("אני תקוע, עזור לי!"):
                        st.info(f"כדי לפתור, נשווה את המכנה לאפס: ${sp.latex(den)} = 0$.")
                        st.write(f"הפתרונות הם: $x = {true_pts}$")
                        st.session_state['force_step_2'] = True
            except:
                st.warning("אנא הכנס מספרים בלבד, מופרדים בפסיק.")

        # מנגנון פתיחת שלב בכוח
        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: הגרף והמשך החקירה ---
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: בניית הגרף")
            st.write("עכשיו כשיש לנו את נקודות אי-ההגדרה, נוכל לראות איך הן נראות בגרף כאסימפטוטות אנכיות.")
            
            # יצירת גרף
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-10, 10, 1000)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_vals = f_num(x_vals)
            y_vals[np.abs(y_vals) > 20] = np.nan
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="הפונקציה", line=dict(color='blue', width=2)))
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text="אסימפטוטה")
            
            st.plotly_chart(fig)
            
            st.subheader("משימה הבאה: גזירה")
            st.write("גזור את הפונקציה במחברת שלך. כשתהיה מוכן, לחץ כדי לראות אם צדקת.")
            if st.checkbox("הצג נגזרת לבדיקה"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("שגיאה בכתיבת הפונקציה. וודא שהשתמשת ב- * לכפל וב- ** לחזקה.")

st.sidebar.markdown("---")
if st.sidebar.button("אפס חקירה"):
    st.session_state['force_step_2'] = False
    st.rerun()
