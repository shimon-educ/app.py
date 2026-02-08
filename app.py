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
                    st.info("נראה שזו לא התשובה הנכונה. נסה שוב בעזרת הרמזים.")
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
            with st.expander("💡 רמז מפורט: אסימפטוטה אופקית"):
                st.markdown("""
                * **חזקה גבוהה במכנה:** $y = 0$. דוגמה: $f(x) = \\frac{2x+1}{x^2-4} \implies y = 0$
                * **חזקות שוות:** מחלקים מקדמים. דוגמה: $f(x) = \\frac{6x^2+1}{2x^2-3} \implies y = 3$
                * **חזקה גבוהה במונה:** אין אסימפטוטה. דוגמה: $f(x) = \\frac{x^3}{x^2+1} \implies \text{אין}$
                """)
            user_horiz = st.text_input("מהי משוואת האסימפטוטה האופקית? (y = ?):", key="horiz_input")
            
            if user_asymp and user_horiz:
                # בדיקה לוגית לפני מעבר לשלב 3
                try:
                    true_h = sp.limit(f, x, sp.oo)
                    u_h = user_horiz.replace('y','').replace('=','').strip()
                    u_v = sorted([float(p.strip()) for p in user_asymp.replace('x','').replace('=','').split(",")])
                    
                    check_v = np.allclose(u_v, [float(p) for p in true_pts])
                    check_h = np.isclose(float(u_h), float(true_h)) if u_h.lower() != "אין" else not true_h.is_finite
                    
                    if check_v and check_h:
                        st.success("מעולה! בוא נמשיך לנקודות חיתוך.")
                        show_step_3 = True
                    else:
                        st.info("זו לא התשובה הנכונה. נסה שוב או הצג פתרון.")
                except: pass

        # --- שלב 3: נקודות חיתוך ---
        if show_step_3:
            st.markdown("---")
            st.header("שלב 3: נקודות חיתוך עם הצירים")
            
            user_x_int = st.text_input("ערכי x של נקודות החיתוך עם ציר x:", key="x_int_input")
            user_y_int = st.text_input("ערך y של נקודת החיתוך עם ציר y:", key="y_int_input")

            if st.button("הצג פתרון וסרטט"):
                x_roots = [r for r in sp.solve(num, x) if r not in true_domain]
                y_val = f.subs(x, 0) if 0 not in true_domain else None
                
                st.write(f"**חיתוך x:** {[(format_num(r), 0) for r in x_roots] if x_roots else 'אין'}")
                st.write(f"**חיתוך y:** {(0, format_num(y_val)) if y_val is not None else 'אין'}")

                fig = go.Figure()
                for pt in true_pts:
                    fig.add_vline(x=float(pt), line_dash="dash", line_color="red", annotation_text=f"x={pt}")
                h_lim = sp.limit(f, x, sp.oo)
                if h_lim.is_finite:
                    fig.add_hline(y=float(h_lim), line_dash="dash", line_color="blue", annotation_text=f"y={format_num(h_lim)}")
                
                # הוספת הנקודות לגרף
                for r in x_roots:
                    fig.add_trace(go.Scatter(x=[float(r)], y=[0], mode='markers+text', text=["חיתוך x"], textposition="top center", marker=dict(color='green', size=12)))
                if y_val is not None:
                    fig.add_trace(go.Scatter(x=[0], y=[float(y_val)], mode='markers+text', text=["חיתוך y"], textposition="middle right", marker=dict(color='orange', size=12)))

                fig.update_xaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='black', range=[-10, 10])
                fig.update_layout(plot_bgcolor='white', height=500, showlegend=False)
                st.plotly_chart(fig)

    except Exception as e:
        st.error("הביטוי המתמטי לא תקין.")
