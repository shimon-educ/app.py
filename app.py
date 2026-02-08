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
        
        # --- שלב 1: תחום הגדרה ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        with st.expander("🤔 איך מוצאים תחום הגדרה? (הסבר תיאורטי)"):
            st.write("""
            **מה זה בכלל תחום הגדרה?**
            במתמטיקה, אסור לחלק באפס. לכן עלינו למצוא אילו ערכי x מאפסים את המכנה ולהוציא אותם מהתחום.
            **השלבים:** משווים את המכנה לאפס ($המכנה = 0$) ופתורים את המשוואה.
            """)
        
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
                        st.info("מהלך הפתרון:")
                        st.success(f"הערכים המאפסים הם: {true_pts_str}")
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            user_asymp = st.text_input("1. מהן משוואות האסימפטוטות האנכיות?", key="asymp_input")
            user_horiz = st.text_input("2. מהי משוואת האסימפטוטה האופקית?", key="horiz_input")
            
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("💡 איך מוצאים אנכית?"):
                    st.write("אלו ערכי ה-x שמאפסים את המכנה (הנקודות שמצאת בשלב 1).")
            
            with col2:
                with st.expander("💡 איך מוצאים אופקית?"):
                    st.write("נשווה את הדרגה (החזקה הכי גבוהה) של המונה לעומת המכנה.")

            if st.button("הצג פתרון וסרטט"):
                st.subheader("תרשים האסימפטוטות")
                fig = go.Figure()
                # סרטוט אנכיות
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                # סרטוט אופקית
                true_h_val = sp.limit(f, x, sp.oo)
                if true_h_val.is_finite:
                    fig.add_hline(y=float(true_h_val), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(true_h_val)}")
                
                fig.update_layout(height=400, template="simple_white")
                fig.update_xaxes(range=[-10, 10], zeroline=True, zerolinecolor="black")
                fig.update_yaxes(range=[-10, 10], zeroline=True, zerolinecolor="black")
                st.plotly_chart(fig)

    except Exception as e:
        st.error(f"שגיאה בניתוח הפונקציה.")

if st.sidebar.button("נקה הכל"):
    st.session_state.clear()
    st.rerun()
