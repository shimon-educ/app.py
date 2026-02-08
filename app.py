import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="MathBuddy - מעבדת החקירה", layout="centered")

st.title("🧪 מעבדת החקירה של שמעון")
st.write("בוא נחקור את הפונקציה צעד אחר צעד.")

# הזנת פונקציה בתפריט הצד
input_func = st.sidebar.text_input("הזן פונקציה לחקירה:", "x**2 / (x**2 + 2*x - 3)")

if input_func:
    x = sp.symbols('x')
    try:
        f = sp.sympify(input_func)
        num, den = sp.fraction(f)
        true_domain = sp.solve(den, x)
        # הפיכת הפתרונות למספרים פשוטים
        true_pts = sorted([float(p.evalf()) for p in true_domain])
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(f"f(x) = {sp.latex(f)}")
        st.write("כדי למצוא את תחום ההגדרה, עלינו למצוא אילו ערכי $x$ מאפסים את המכנה.")
        
        # הדוגמה כאן היא כללית ולא קשורה לפונקציה הספציפית
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        show_step_2 = False
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, true_pts):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.error("הערכים האלו לא מאפסים את המכנה. נסה שוב.")
                    
                    # רמז 1: הצגת המכנה כמשוואה
                    if st.checkbox("צריך רמז ראשון?"):
                        st.write(f"עליך לפתור את המשוואה: ${sp.latex(den)} = 0$")
                        
                    # רמז 2: פירוק לגורמים
                    if st.checkbox("צריך עזרה בפירוק המכנה?"):
                        factored_den = sp.factor(den)
                        st.write(f"אפשר לכתוב את המכנה כך: ${sp.latex(factored_den)} = 0$")
                        st.write("עכשיו קל יותר לראות מה מאפס כל סוגריים, נכון?")

                    # מוצא אחרון: חשיפת תשובה
                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.info(f"הערכים המאפסים הם: {', '.join(map(str, true_pts))}")
                        st.session_state['force_step_2'] = True
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק (למשל: 3, 1-)")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות וגרף ---
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: הצגה גרפית")
            st.write(f"נקודות אי-ההגדרה $x = {true_pts}$ הן האסימפטוטות האנכיות שלנו.")
            
            # יצירת גרף
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-10, 10, 1000)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_vals = f_num(x_vals)
            y_vals[np.abs(y_vals) > 20] = np.nan
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)", line=dict(color='#1f77b4', width=2)))
            
            for pt in true_pts:
                fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text="אסימפטוטה")
            
            fig.update_layout(xaxis_title="x", yaxis_title="y", hovermode="x")
            st.plotly_chart(fig)
            
            st.subheader("האתגר הבא: גזירה")
            st.write("גזור את הפונקציה לפי חוקי נגזרת מנה.")
            if st.checkbox("בדוק את הנגזרת שלך"):
                st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין. וודא שכתבת לפי הכללים בצד.")

# כפתור איפוס בתפריט הצד
if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state['force_step_2'] = False
    st.rerun()
