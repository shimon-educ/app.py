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
                    st.info("נראה שזו לא התשובה הנכונה. אני ממליץ לך להסתכל ברמזים למטה ולנסות שוב.")
            except:
                st.warning("נא להזין מספרים מופרדים בפסיק.")

        if st.session_state.get('force_step_2'):
            show_step_2 = True

        # --- שלב 2: אסימפטוטות ---
        show_step_3 = False
        if show_step_2:
            st.markdown("---")
            st.header("שלב 2: אסימפטוטות")
            
            st.subheader("1. אסימפטוטות אנכיות")
            user_asymp = st.text_input("מהן משוואות האסימפטוטות האנכיות? (למשל: 1, 3-):", key="asymp_input")
            
            st.subheader("2. אסימפטוטה אופקית")
            with st.expander("💡 רמז מפורט: איך מוצאים אסימפטוטה אופקית?"):
                st.write("אנו בודקים את 'מלחמת הכוחות' בין המונה למכנה (החזקה הגבוהה ביותר):")
                st.markdown("""
                1. **החזקה הגבוהה ביותר נמצאת במכנה (למטה):** $y = 0$
                2. **החזקות הגבוהות ביותר שוות:** מחלקים את המקדמים.
                3. **החזקה הגבוהה ביותר נמצאת במונה (למעלה):** אין אסימפטוטה.
                """)
            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (y = ?):", key="horiz_input")
            
            if user_asymp and user_horiz:
                show_step_3 = True

        # --- שלב 3: נקודות חיתוך עם הצירים ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם הצירים")
            
            st.subheader("1. חיתוך עם ציר x")
            with st.expander("💡 רמז: חיתוך עם ציר x"):
                st.write("מציבים $y=0$ (כלומר, מוצאים מתי המונה שווה לאפס).")
            user_x_int = st.text_input("הזן את ערכי ה-x של נקודות החיתוך (למשל: 0, 4):", key="x_int_input")
            
            st.subheader("2. חיתוך עם ציר y")
            with st.expander("💡 רמז: חיתוך עם ציר y"):
                st.write("מציבים $x=0$ בפונקציה.")
            user_y_int = st.text_input("הזן את ערך ה-y של נקודת החיתוך:", key="y_int_input")

            if st.button("הצג פתרון וסרטט"):
                # חישוב פתרונות חיתוך לצורך הצגה
                x_roots = [r for r in sp.solve(num, x) if r not in true_domain]
                y_val = f.subs(x, 0) if 0 not in true_domain else None
                
                st.write(f"**נקודות חיתוך עם ציר x:** {[(format_num(r), 0) for r in x_roots] if x_roots else 'אין'}")
                st.write(f"**נקודת חיתוך עם ציר y:** {(0, format_num(y_val)) if y_val is not None else 'אין'}")

                # סרטוט הגרף האינטראקטיבי
                fig = go.Figure()
                
                # אסימפטוטות
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                h_val_lim = sp.limit(f, x, sp.oo)
                if h_val_lim.is_finite:
                    fig.add_hline(y=float(h_val_lim), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(h_val_lim)}")
                
                # נקודות חיתוך על הגרף
                for r in x_roots:
                    fig.add_trace(go.Scatter(x=[float(r)], y=[0], mode='markers', marker=dict(color='green', size=10), name="חיתוך x"))
                if y_val is not None:
                    fig.add_trace(go.Scatter(x=[0], y=[float(y_val)], mode='markers', marker=dict(color='orange', size=10), name="חיתוך y"))

                fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_layout(plot_bgcolor='white', height=500, showlegend=False)
                st.plotly_chart(fig)

                st.markdown("---")
                st.subheader("השלב הבא: גזירה")
                if st.checkbox("בדוק את הנגזרת שחישבת"):
                    st.latex(r"f'(x) = " + sp.latex(sp.simplify(sp.diff(f, x))))

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")

if st.sidebar.button("התחל חקירה חדשה"):
    st.session_state.clear()
    st.rerun()
