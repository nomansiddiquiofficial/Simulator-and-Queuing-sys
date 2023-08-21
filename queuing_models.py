import streamlit as st
import math

def mmc(Arrival_Mean,Service_Mean,No_of_server):
    lembda=1/Arrival_Mean
    meu=1/Service_Mean
    c=No_of_server
    p=lembda/(c*meu) 
    
    value=0
    for m in range(c):
        value=value+(((c*p)**m)/(math.factorial(m)))+(((c*p)**c)/(math.factorial(c)*(1-p)))
        
    Pnot=1/value
    Lq=(Pnot*p*(lembda/meu)**c)/(math.factorial(c)*((1-p)**2))
    Wq=Lq/lembda
    Ws=Wq+(1/meu)
    Ls=Ws*lembda

    st.subheader("M/M/C Model Results:")

    st.text(f"Server Utilization Rate: {p:.2f}")
    st.text(f"Server idle time: {1-p:.2f}")
    st.text(f"Number of customers in queue: {Lq:.2f}")
    st.text(f"Wait time in the queue: {Wq:.2f}")
    st.text(f"Number of customers in the system: {Ls:.2f}")
    st.text(f"Wait time in the system: {Ws:.2f}s")







def mgc(Arrival_Mean,Service_Mean,ArrivalVariance,ServiceVariance,No_of_server):
    lembda=1/Arrival_Mean
    meu=1/Service_Mean
    c=No_of_server
    p=lembda/(c*meu)
    Ca=ArrivalVariance/((1/lembda)**2)
    Cs=ServiceVariance/((1/meu)**2)
    value=0
    for m in range(c):
        value=value+(((c*p)**m)/(math.factorial(m)))+(((c*p)**c)/(math.factorial(c)*(1-p)))
    Pnot=1/value
    Lq=(Pnot*p*(lembda/meu)**c)/(math.factorial(c)*((1-p)**2))
    Wq=Lq/lembda
    Wq=Wq*((Ca+Cs)/2)
    Lq=lembda*Wq
    Ws=Wq+(1/meu)
    Ls=Ws*lembda

    st.subheader("M/G/C Model Results:")

    st.text(f"Server Utilization Rate: {p:.2f}")
    st.text(f"Server idle time: {1-p:.2f}")
    st.text(f"Number of customers in queue: {Lq:.2f}")
    st.text(f"Wait time in the queue: {Wq:.2f}")
    st.text(f"Number of customers in the system: {Ls:.2f}")
    st.text(f"Wait time in the system: {Ws:.2f}")





def ggc(Arrival_Mean,Service_Mean,ArrivalVariance,ServiceVariance,No_of_server):
    lembda=1/Arrival_Mean
    meu=1/Service_Mean
    c=No_of_server
    p=lembda/(c*meu)
    Ca=ArrivalVariance/((1/lembda)**2)
    Cs=ServiceVariance/((1/meu)**2)
    value=0
    for m in range(c):
        value=value+(((c*p)**m)/(math.factorial(m)))+(((c*p)**c)/(math.factorial(c)*(1-p)))
    Pnot=1/value
    Lq=(Pnot*p*(lembda/meu)**c)/(math.factorial(c)*((1-p)**2))
    Wq=Lq/lembda
    Wq=Wq*((Ca+Cs)/2)
    Lq=lembda*Wq
    Ws=Wq+(1/meu)
    Ls=Ws*lembda

    st.subheader("G/G/C Model Results:")
    
    st.text(f"Server Utilization Rate: {p:.2f}")
    st.text(f"Server idle time: {1-p:.2f}")
    st.text(f"Number of customers in queue: {Lq:.2f}")
    st.text(f"Wait time in the queue: {Wq:.2f}")
    st.text(f"Number of customers in the system: {Ls:.2f}")
    st.text(f"Wait time in the system: {Ws:.2f}")













def main():
    st.title("Queuing Model Simulator")
    
    No_of_server = st.number_input("Number of servers",value = 1)

    selected = st.selectbox("Select queuing model:", ["M/M/C", "M/G/C","G/G/C"])

   
    
    if selected == "M/M/C":
        Arrival_Mean = st.number_input("Enter mean inter-arrival time:", value=2.65)
        Service_Mean = st.number_input("Enter average service time:", value=1.58)
    
    elif selected == "M/G/C":
        Arrival_Mean = st.number_input("Enter mean inter-arrival time:", value=2.65)
        Service_Mean = st.number_input("Enter average service time:", value=8)
        ArrivalVariance = st.number_input("Enter variance for arrival:", value=20)
        ServiceVariance = st.number_input("Enter variance for service:", value=25)
    
    elif selected == "G/G/C":
        Arrival_Mean = st.number_input("Enter mean inter-arrival time:", value=2.65)
        Service_Mean = st.number_input("Enter average service time:", value=8)
        ArrivalVariance = st.number_input("Enter variance for arrival:", value=20)
        ServiceVariance = st.number_input("Enter variance for service:", value=25)
    if st.button("Run Simulation"):


        if selected == "M/M/C":
            mmc(Arrival_Mean,Service_Mean,No_of_server)
        elif selected == "M/G/C":
            mgc(Arrival_Mean,Service_Mean,ArrivalVariance,ServiceVariance,No_of_server)    
        elif selected == "G/G/C":
            mgc(Arrival_Mean,Service_Mean,ArrivalVariance,ServiceVariance,No_of_server)    

        


            
            


main()
    