import streamlit as st
import home
import mm1_mg1
import mm2_mg2
import gg1
import gg2
import queuing_models

def app():

    a = st.sidebar.selectbox("Selects From Following Pages", [
                             "Home", "Simulation of Random Data","Queuing model"], index=0)
    
    if a == "Simulation of Random Data":

        st.title("Simulation of Random Data")

        choice_format = st.radio("Choose time unit:", ["minutes", "seconds"])

        model = st.selectbox("Selects Model", [
                             "M/M/C", "M/G/C","G/G/C"], index=0)
        
        server_count = st.radio("Select server (C)",
                            ('1', '2'))   
        
        if model == "G/G/C":
                
                mean = st.number_input('Enter value of mean')

                variance = st.number_input('Enter value of variance')

                max = st.number_input('Enter value of max')

                min = st.number_input('Enter value of min')

                if server_count == '1':

                    if st.button("Simulate"):

                        gg1.simulate_gg1(mean, variance, max, min, server_count,choice_format)

                if server_count == '2':

                    if st.button("Simulate"):

                        gg2.simulate_gg2(mean, variance, max, min, server_count,choice_format)       

        elif server_count == '1':
            
            lam = st.number_input('Enter value of Lambda')

            if model == "M/M/C":

                mu = st.number_input('Enter value of mu')

                if st.button("Simulate"):

                    st.title("M/M/1")

                    mm1_mg1.mm1(lam, mu, server_count,choice_format)

            elif model == "M/G/C":
                
                max = st.number_input('Enter value of max')

                min = st.number_input('Enter value of min')
            
                mu=(max+min)/2

                if st.button("Simulate"):

                    st.title("M/G/1")

                    mm1_mg1.mm1(lam, mu, server_count,choice_format)

        elif server_count == '2':
            
            lam = st.number_input('Enter value of Lambda')

            if model == "M/M/C":

                mu = st.number_input('Enter value of mu')

                if st.button("Simulate"):

                    st.title("M/M/2")

                    mm2_mg2.mm2(lam, mu, server_count,choice_format)

            elif model == "M/G/C":
                
                max = st.number_input('Enter value of max')

                min = st.number_input('Enter value of min')
            
                mu=(max+min)/2

                if st.button("Simulate"):

                    st.title("M/G/2") 

                    mm2_mg2.mm2(lam, mu, server_count,choice_format)

    elif a == "Queuing model":
        queuing_models.main()
    elif a == "Home":
        home.fun()


app()
