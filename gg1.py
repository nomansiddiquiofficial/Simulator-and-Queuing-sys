import streamlit as st
import pandas as pd
import math as mt
import random as rd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns


def simulate_gg1(mean, variance, max, min, server_count,choice_format):
    st.title("G/G/1")
    mu=(max+min)/2

    cumulative = []
    lookup = []
    sum_prob = 0  # Initialize the sum of probabilities
    i = 0  # Initialize the loop variable
    
    while (sum_prob < 0.999):  # Continue the loop until the sum reaches or exceeds 1
    
        normal=(1/(mt.sqrt(variance)*mt.sqrt(2*mt.pi)))*mt.exp(-(i-mean)**2/(2*variance))
        
        if i == 0:
            cumulative.append(normal)
            lookup.append(0)
            sum_prob += normal
        elif (i != 0):
            if (cumulative[-1]!=1):
                cumulative.append(normal + cumulative[i - 1])
                sum_prob += normal
                lookup.append(cumulative[i - 1])

            else:
                break            

        i += 1  # Increment the loop variable

    customer_count=len(cumulative)

            
    if choice_format == "minutes":

        interarrival=[0]

        for i in range(1,customer_count):  
            random_value = rd.random()

            for j in range(customer_count):
        
                if (lookup[j] <= random_value) and (cumulative[j] >= random_value):
                    interarrival.append(j+1)        
        arrival=[0]

        for i in range(1,customer_count):
            arrival.append(arrival[i-1]+interarrival[i])

        service=[]

        for i in range(customer_count):
            a=-mu*(mt.log(rd.random()))
            service.append(mt.ceil(a))

        start=[arrival[0]]

        end=[service[0]]        

        for i in range(1,customer_count):

            if end[i-1]>=arrival[i]:
                start.append(end[i-1])
                end.append(start[i]+service[i])

            elif end[i-1]<arrival[i]:
                start.append(arrival[i])
                end.append(start[i]+service[i])
                
        turnaround = [end[i] - arrival[i] for i in range(customer_count)]
        waittime = [turnaround[i] - service[i] for i in range(customer_count)]
        responsetime = [start[i] - arrival[i] for i in range(customer_count)]

        df = pd.DataFrame({'Cumulative': cumulative, 'Lookup': lookup, 'Interarrival':interarrival,'Arrival':arrival, 'Service':service, 'Start':start,'End':end, 'TurnAround':turnaround, 'WaitTime':waittime, 'ResponseTime':responsetime})
        st.dataframe(df)

        st.text(f"Average Service Time: {round((sum(service)/customer_count),2)}")
        st.text(f"Average Turn Around Time: {round((sum(turnaround)/customer_count),2)}")
        st.text(f"Average Wait Time: {round((sum(waittime)/customer_count),2)}")
        st.text(f"Average Response Time: {round((sum(responsetime)/customer_count),2)}")

        # Calculate total time
        total_service_time = sum(service)
    
        server = []

        for i in range(len(start)):
            server.append([start[i], end[i]])

        server_utilization_rate = sum([interval[1] - interval[0] for interval in server]) / total_service_time

        # Calculate server idle rate
        server_idle_rate = 1 - server_utilization_rate
        
        st.text(f"Server Utilization Rate: {round(server_utilization_rate, 2)}")
        st.text(f"Server Idle Rate: {round(server_idle_rate, 2)}")

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, (s, e) in enumerate(zip(start, end)):
            ax.barh(i, e - s, left=s, height=0.6, align='center', color='blue')

        ax.set_xlabel('Time')
        ax.set_ylabel('Customers')
        ax.set_yticks(range(len(start)))
        ax.set_yticklabels([f'Customer {i+1}' for i in range(len(start))])
        ax.set_title('Gantt Chart')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()

        st.pyplot(fig)

        # Show Interarrivals graph
        plt.figure(figsize=(10, 6)) 
        sns.distplot(interarrival, kde=False, color='r', bins=20)  
        plt.title('Interarrivals')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        sns.despine()
        interarrivals_fig = plt.gcf()
        st.pyplot(interarrivals_fig)

        # Show Service Times graph
        plt.figure(figsize=(10, 6))  
        sns.distplot(service, kde=False, bins=20)  
        plt.title('Service Times')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        sns.despine()
        service_times_fig = plt.gcf()
        st.pyplot(service_times_fig)

    elif choice_format == "seconds":
        interarrival=[0]

        for i in range(1,customer_count):  
            random_value = rd.random()

            for j in range(customer_count):
        
                if (lookup[j] <= random_value) and (cumulative[j] >= random_value):
                    interarrival.append((j+1)*60)

        arrival=[0]

        for i in range(1,customer_count):
            arrival.append(arrival[i-1]+interarrival[i])

        service=[]

        for i in range(customer_count):
            a=-mu*(mt.log(rd.random()))
            service.append(mt.ceil(a*60))
            
        start=[arrival[0]]

        end=[service[0]]        

        for i in range(1,customer_count):

            if end[i-1]>=arrival[i]:
                start.append(end[i-1])
                end.append(start[i]+service[i])

            elif end[i-1]<arrival[i]:
                start.append(arrival[i])
                end.append(start[i]+service[i])
                
        turnaround = [end[i] - arrival[i] for i in range(customer_count)]
        waittime = [turnaround[i] - service[i] for i in range(customer_count)]
        responsetime = [start[i] - arrival[i] for i in range(customer_count)]

        df = pd.DataFrame({'Cumulative': cumulative, 'Lookup': lookup, 'Interarrival':interarrival,'Arrival':arrival, 'Service':service, 'Start':start,'End':end, 'TurnAround':turnaround, 'WaitTime':waittime, 'ResponseTime':responsetime})
        st.dataframe(df)

        st.text(f"Average Service Time: {round((sum(service)/customer_count),2)}")
        st.text(f"Average Turn Around Time: {round((sum(turnaround)/customer_count),2)}")
        st.text(f"Average Wait Time: {round((sum(waittime)/customer_count),2)}")
        st.text(f"Average Response Time: {round((sum(responsetime)/customer_count),2)}")

        # Calculate total time
        total_service_time = sum(service)
    
        server = []

        for i in range(len(start)):
            server.append([start[i], end[i]])

        server_utilization_rate = sum([interval[1] - interval[0] for interval in server]) / total_service_time

        # Calculate server idle rate
        server_idle_rate = 1 - server_utilization_rate
        
        st.text(f"Server Utilization Rate: {round(server_utilization_rate, 2)}")
        st.text(f"Server Idle Rate: {round(server_idle_rate, 2)}")

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, (s, e) in enumerate(zip(start, end)):
            ax.barh(i, e - s, left=s, height=0.6, align='center', color='blue')

        ax.set_xlabel('Time')
        ax.set_ylabel('Customers')
        ax.set_yticks(range(len(start)))
        ax.set_yticklabels([f'Customer {i+1}' for i in range(len(start))])
        ax.set_title('Gantt Chart')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()

        st.pyplot(fig)

        # Show Interarrivals graph
        plt.figure(figsize=(10, 6)) 
        sns.distplot(interarrival, kde=False, color='r', bins=20)  
        plt.title('Interarrivals')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        sns.despine()
        interarrivals_fig = plt.gcf()
        st.pyplot(interarrivals_fig)

        # Show Service Times graph
        plt.figure(figsize=(10, 6))  
        sns.distplot(service, kde=False, bins=20)  
        plt.title('Service Times')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        sns.despine()
        service_times_fig = plt.gcf()
        st.pyplot(service_times_fig)

