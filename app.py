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
            st.write("בפונקציית שבר, המכנה אסור שיהיה שווה לאפס. לכן נשווה את המכנה ל-0 ונמצא את ה-x-ים ה'אסורים'.")
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 3, 1-):", key="domain_input")
        
        show_step_2 = False
        
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("מעולה! אלו בדיוק הערכים שמאפסים את המכנה.")
                    show_step_2 = True
                else:
                    st.error("לא בדיוק... נסה להיעזר ברמזים למטה.")
                    
                    st.markdown("### 💡 עזרה בפתרון המכנה:")
                    if st.checkbox("צריך רמז (הצגת המשוואה)?"):
                        st.write("עליך לפתור את המשוואה הבאה:")
                        st.latex(sp.latex(den) + "= 0")
                        
                    if st.button("התייאשתי, הצג פתרון מלא והמשך"):
                        st.info("מהלך הפתרון באמצעות נוסחת השורשים:")
                        try:
                            p = sp.Poly(den, x)
                            coeffs = p.all_coeffs()
                            if len(coeffs) == 3:
                                a, b, c = [float(v) for v in coeffs]
                                delta = b**2 - 4*a*c
                                st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                                st.latex(f"x_{{1,2}} = \\frac{{-({format_num(b)}) \\pm \\sqrt{{{format_num(delta)}}}}}{{{2*format_num(a)}}}")
                                st.write(f"השורשים שמצאנו הם: **{true_pts_str}**")
                            else:
                                st.write(f"הפתרונות הם: **{true_pts_str}**")
                        except:
                            st.write(f"הערכים הם: **{true_pts_str}**")
                        
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק (למשל: 1, -3).")

        if st.session_state.get('force_step_2') or show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            # קלט מהמשתמש
            user_as_v = st.text_input("1. מהן האסימפטוטות האנכיות?", key="v_in")
            user_as_h = st.text_input("2. מהי האסימפטוטה האופקית? (מספר או 'אין')", key="h_in")
            
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("💡 איך מוצאים אנכית?"):
                    st.write("אלו הן נקודות אי-ההגדרה שמצאת בשלב 1 (בתנאי שהן לא מאפסות את המונה).")
                    st.info(f"הנקודות שמצאת: {true_pts_str}")
                    st.write("🔗 [הסבר על אסימפטוטה אנכית](https://ischool.co.il/math/analisys/rational-functions/vertical-asymptote/)")
            
            with col2:
                with st.expander("💡 איך מוצאים אופקית?"):
                    st.write("נבדוק את החזקה הגבוהה ביותר במונה ($n$) ובמכנה ($m$):")
                    st.info("""
                    * **מכנה חזק יותר ($n < m$):** האסימפטוטה היא **y = 0**.
                    * **חזקות שוות ($n = m$):** האסימפטוטה היא **יחס המקדמים**.
                    * **מונה חזק יותר ($n > m$):** **אין אסימפטוטה אופקית**.
                    """)
                    st.write("🔗 [הסבר על אסימפטוטה אופקית](https://ischool.co.il/math/analisys/rational-functions/horizontal-asymptote/)")

            if st.button("סרטט אסימפטוטות על הגרף"):
                fig = go.Figure()
                # סרטוט קווים אנכיים
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                
                # חישוב וסרטוט קו אופקי
                h_limit = sp.limit(f, x, sp.oo)
                if h_limit.is_finite:
                    fig.add_hline(y=float(h_limit), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(h_limit)}")
                
                fig.update_layout(height=450, template="simple_white", title="מיקום האסימפטוטות")
                fig.update_xaxes(range=[-10, 10], zeroline=True, zerolinecolor="black")
                fig.update_yaxes(range=[-10, 10], zeroline=True, zerolinecolor="black")
                st.plotly_chart(fig)

    except Exception as e:
        st.error("הפונקציה שהוזנה אינה תקינה. השתמש ב-* לכפל וב-** לחזקה.")

if st.sidebar.button("התחל מהתחלה"):
    st.session_state.clear()
    st.rerun()
