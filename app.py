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
        
        # --- שלב 1: תחום הגדרה (ללא שינוי) ---
        st.header("שלב 1: תחום הגדרה")
        st.latex(r"f(x) = " + sp.latex(f))

        with st.expander("🤔 איך מוצאים תחום הגדרה? (הסבר תיאורטי)"):
            st.write("""
            **מה זה בכלל תחום הגדרה?**
            במתמטיקה, יש פעולה אחת שאסור לעשות: **חלוקה באפס**. 
            כשיש לנו פונקציה עם שבר (פונקציה רציונלית), עלינו לוודא שהמכנה אף פעם לא יהיה אפס.
            
            **איך מוצאים אותו?**
            1. לוקחים רק את המכנה של הפונקציה.
            2. משווים אותו לאפס: $המכנה = 0$.
            3. פותרים את המשוואה שנוצרה.
            4. הערכים שקיבלנו הם הערכים ש"אסור" להציב בפונקציה.
            """)
        
        user_domain = st.text_input("הזן את הערכים שמאפסים את המכנה (למשל: 5, 2-):", key="domain_input")
        
        step_1_passed = False
        if user_domain:
            try:
                user_pts = sorted([float(p.strip()) for p in user_domain.split(",")])
                if np.allclose(user_pts, [float(p) for p in true_pts]):
                    st.success("כל הכבוד! אלו בדיוק הערכים שמאפסים את המכנה.")
                    step_1_passed = True
                else:
                    st.error("לא בדיוק... הערכים האלו לא מאפסים את המכנה.")
                    if st.checkbox("צריך רמז ראשון?"):
                        st.latex(sp.latex(den) + "= 0")
                    if st.checkbox("צריך עזרה בפירוק המכנה?"):
                        st.latex(sp.latex(sp.factor(den)) + "= 0")
                    if st.button("התייאשתי, הצג פתרון והמשך"):
                        st.session_state['force_step_2'] = True
                        st.rerun()
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            step_1_passed = True

        # --- שלב 2: אסימפטוטות אנכיות (החדש!) ---
        if step_1_passed:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות אנכיות")
            
            with st.expander("🤔 מהן אסימפטוטות אנכיות? (הסבר תיאורטי)"):
                st.write("""
                **הקשר בין תחום הגדרה לאסימפטוטה:**
                אסימפטוטה אנכית היא קו ישר שהפונקציה שואפת אליו (מתקרבת אליו מאוד) אך לא נוגעת בו.
                בפונקציות רציונליות, הערכים שמאפסים את המכנה (נקודות אי-ההגדרה) הם בדרך כלל המקומות שבהם תהיה אסימפטוטה אנכית.
                
                **למה זה קורה?**
                כשמתקרבים לערך שמאפס את המכנה, השבר הופך למספר עצום (חיובי או שלילי), ולכן הגרף "בורח" למעלה או למטה לאורך הקו האנכי.
                """)

            st.write("על סמך תחום הגדרה שמצאת, מהן משוואות האסימפטוטות האנכיות?")
            user_asymptotes = st.text_input("הזן את ערכי ה-x (למשל: 3, 1-):", key="asymp_input")
            
            show_plot = False
            if user_asymptotes:
                try:
                    user_asy_pts = sorted([float(p.strip()) for p in user_asymptotes.split(",")])
                    if np.allclose(user_asy_pts, [float(p) for p in true_pts]):
                        st.success(f"נכון מאוד! האסימפטוטות הן x = {user_asymptotes}")
                        show_plot = True
                    else:
                        st.error("אלו לא האסימפטוטות הנכונות. זכור: אלו הערכים שמאפסים את המכנה!")
                        if st.button("התייאשתי, הצג הסבר וסרטט"):
                            st.info(f"האסימפטוטות האנכיות הן בנקודות שבהן הפונקציה לא מוגדרת: x = {true_pts_str}")
                            st.session_state['force_plot'] = True
                            st.rerun()
                except:
                    st.warning("נא להזין מספרים מופרדים בפסיק.")

            if st.session_state.get('force_plot'):
                show_plot = True

            # סימון על מערכת הצירים (ללא הגרף של הפונקציה!)
            if show_plot:
                st.subheader("מערכת הצירים שלך:")
                fig = go.Figure()
                
                # מוסיפים רק את האסימפטוטות כקווים אדומים מקווקווים
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", 
                                  annotation_text=f"x={pt}", annotation_position="top")
                
                # הגדרות צירים
                fig.update_layout(xaxis=dict(range=[-10, 10]), yaxis=dict(range=[-10, 10]),
                                  xaxis_title="x", yaxis_title="y",
                                  title="מיקום האסימפטוטות על הצירים")
                st.plotly_chart(fig)
                
                st.info("מעולה! עכשיו שיש לנו את ה'קירות' (האסימפטוטות), נוכל להמשיך לחקור את התנהגות הפונקציה ביניהם.")
                
                if st.checkbox("עבור לשלב הבא: חקירת נגזרת"):
                    st.write("בקרוב...")

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
