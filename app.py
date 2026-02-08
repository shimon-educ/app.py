import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy - מעבדת החקירה", layout="centered")

# עיצוב כותרת ידידותי
st.title("🧪 מעבדת החקירה של שמעון")
st.write("כאן לא מקבלים פתרונות, כאן לומדים לחקור!")

# הזנת פונקציה
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x-1)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        user_domain = st.text_input("מהם הערכים שמאפסים את המכנה? (הפרד בפסיקים)")
        
        show_step_2 = False
        if user_domain:
            try:
                user_pts = [float(p.strip()) for p in user_domain.split(",")]
                if set(user_pts) == set([float(p) for p in true_domain]):
                    st.success("מעולה! מצאת את נקודות אי-ההגדרה.")
                    show_step_2 = True
                else:
                    st.warning("לא בדיוק... נסה לבדוק שוב מה מאפס את המכנה.")
            except:
                st.error("אנא הכנס מספרים בלבד.")

        # --- שלב 2: אסימפטוטות (מופיע רק אם שלב 1 עבר) ---
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            st.write(f"מצאנו שהפונקציה לא מוגדרת ב-x={true_domain}. האם אלו אסימפטוטות?")
            
            if st.button("כן, אלו אסימפטוטות אנכיות"):
                st.info("נכון! הוספתי אותן לגרף בצבע אדום.")
                
                # יצירת גרף
                f_num = sp.lambdify(x, f, "numpy")
                x_vals = np.linspace(-10, 10, 1000)
                y_vals = f_num(x_vals)
                y_vals[np.abs(y_vals) > 20] = np.nan
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="הפונקציה"))
                for pt in true_domain:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
                
                st.plotly_chart(fig)
                st.write("עכשיו נסה לגזור את הפונקציה במחברת שלך...")
                
    except Exception as e:
        st.error("שגיאה בכתיבת הפונקציה.")

st.sidebar.markdown("""
**איך כותבים?**
- חזקה: `x**2`
- כפל: `2*x`
- חילוק: `/`
""")
