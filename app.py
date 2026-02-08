import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

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
        
        # שלב 1: תחום הגדרה
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))
        st.write("כדי למצוא את תחום ההגדרה, עלינו למצוא אילו ערכי x מאפסים את המכנה.")
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.error("לא בדיוק... הערכים האלו לא מאפסים את המכנה.")
                    
                    if st.checkbox("צריך רמז ראשון?"):
                        st.write("עליך לפתור את המשוואה:")
                        st.latex(sp.latex(den) + "= 0")
                        
                    if st.checkbox("צריך עזרה בפירוק המכנה?"):
                        st.write("אפשר לכתוב את המכנה כך:")
                        st.latex(sp.latex(sp.factor(den)) + "= 0")

                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.info("הערכים המאפסים הם: " + true_pts_str)
                        st.session_state['force_step_2'] = True
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # שלב 2: גרף
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: הצגה גרפית")
            st.write("נקודות אי-ההגדרה הן האסימפטוטות האנכיות שלנו.")
            
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-10, 10, 1000)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_vals = f_num(x_vals)
            y_vals[np.abs(y_vals) > 20] = np.nan
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)", line=dict(color='#1f77b4', width=2)))
            
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red")
            
            fig.update_layout(xaxis_title="x", yaxis_title="y")
            st.plotly_chart(fig)
            
            st.subheader("האתגר הבא: גזירה")
            if st.checkbox("בדוק את הנגזרת שחישבת במחברת"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
