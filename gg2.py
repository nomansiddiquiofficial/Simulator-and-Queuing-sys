import streamlit as st
import pandas as pd
import math as mt
import random as rd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

def simulate_gg2(mean, variance, max_val, min_val, server_count,choice_format):
    st.title("G/G/2")
    mu = (max_val + min_val) / 2

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

        class Server:
            def __init__(self):
                self.time_slots = []

        def assign_patient(arrival_time, service_time, servers):
            earliest_server = None
            earliest_finish_time = float('inf')

            for server in servers:
                if len(server.time_slots) == 0 or server.time_slots[-1][1] <= arrival_time:
                    return server

                last_slot = server.time_slots[-1]
                if last_slot[1] < earliest_finish_time:
                    earliest_finish_time = last_slot[1]
                    earliest_server = server

            return earliest_server

        servers = [Server(), Server()]

        for i in range(len(arrival)):
            server = assign_patient(arrival[i], service[i], servers)
            if server is None:
                print(f"Patient {i+1}: No available server.")
            else:
                start_time = max(server.time_slots[-1][1], arrival[i]) if len(server.time_slots) > 0 else arrival[i]
                end_time = start_time + service[i]
                server.time_slots.append([start_time, end_time])

        server_1 = []
        server_2 = []

        for i, server in enumerate(servers):
            server_data = []
            for slot in server.time_slots:
                server_data.append([slot[0], slot[1]])
            if i == 0:
                server_1 = server_data
            else:
                server_2 = server_data

        start = []

        for sublist in server_1 + server_2:
            start.append(sublist[0])
            start.sort()
            
        end=[]

        for i in range(customer_count):
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
        
        server_1a = [nested[0] for nested in server_1]
        server_1b = [nested[1] for nested in server_1]

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, (s, e) in enumerate(zip(server_1a, server_1b)):
            ax.barh(i, e - s, left=s, height=0.6, align='center', color='blue')
        
        list1 = [f'Customer {i+1}' for i in range(len(server_1a))]

        ax.set_xlabel('Time')
        ax.set_ylabel('Customers')
        ax.set_yticks(range(len(server_1a)))
        ax.set_yticklabels(list1)
        ax.set_title('Gantt Chart')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()

        st.pyplot(fig)

        server_2a = [nested[0] for nested in server_2]
        server_2b = [nested[1] for nested in server_2]

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, (s, e) in enumerate(zip(server_2a, server_2b)):
            ax.barh(i, e - s, left=s, height=0.6, align='center', color='blue')
        
        list2 = [f'Customer {i+len(server_1a)+1}' for i in range(len(server_2a))]

        ax.set_xlabel('Time')
        ax.set_ylabel('Customers')
        ax.set_yticks(range(len(server_2a)))
        ax.set_yticklabels(list2)
        ax.set_title('Gantt Chart')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()

        st.pyplot(fig)

        total_service_time = sum(service)

        l = [item for sublist in server_1 for item in sublist]
        res1 = [*set(l)]
        server1_time = sorted(res1)

        server1_utilization = sum([interval[1] - interval[0] for interval in server_1]) / total_service_time

        m = [item for sublist in server_2 for item in sublist]
        res2 = [*set(m)]
        server2_time = sorted(res2)

        server2_utilization = sum([interval[1] - interval[0] for interval in server_2]) / total_service_time

        Total_server_utilization_rate = server1_utilization + server2_utilization

        Total_server_idle_rate = 1 - Total_server_utilization_rate
        st.text(f"Server 1 Utilization Rate: {round(server1_utilization, 2)}")

        st.text(f"Server 2 Utilization Rate: {round(server2_utilization, 2)}")

        st.text(f"Total Server Utilization Rate: {round(Total_server_utilization_rate, 2)}")
        st.text(f"Total Server Idle Rate: {round(Total_server_idle_rate, 2)}")     


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

        class Server:
            def __init__(self):
                self.time_slots = []

        def assign_patient(arrival_time, service_time, servers):
            earliest_server = None
            earliest_finish_time = float('inf')

            for server in servers:
                if len(server.time_slots) == 0 or server.time_slots[-1][1] <= arrival_time:
                    return server

                last_slot = server.time_slots[-1]
                if last_slot[1] < earliest_finish_time:
                    earliest_finish_time = last_slot[1]
                    earliest_server = server

            return earliest_server

        servers = [Server(), Server()]

        for i in range(len(arrival)):
            server = assign_patient(arrival[i], service[i], servers)
            if server is None:
                print(f"Patient {i+1}: No available server.")
            else:
                start_time = max(server.time_slots[-1][1], arrival[i]) if len(server.time_slots) > 0 else arrival[i]
                end_time = start_time + service[i]
                server.time_slots.append([start_time, end_time])

        server_1 = []
        server_2 = []

        for i, server in enumerate(servers):
            server_data = []
            for slot in server.time_slots:
                server_data.append([slot[0]*60, slot[1]*60])
            if i == 0:
                server_1 = server_data
            else:
                server_2 = server_data

        start = []

        for sublist in server_1 + server_2:
            start.append(sublist[0])
            start.sort()
            
        end=[]

        for i in range(customer_count):
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
        
        server_1a = [nested[0] for nested in server_1]
        server_1b = [nested[1] for nested in server_1]

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, (s, e) in enumerate(zip(server_1a, server_1b)):
            ax.barh(i, e - s, left=s, height=0.6, align='center', color='blue')
        
        list1 = [f'Customer {i+1}' for i in range(len(server_1a))]

        ax.set_xlabel('Time')
        ax.set_ylabel('Customers')
        ax.set_yticks(range(len(server_1a)))
        ax.set_yticklabels(list1)
        ax.set_title('Gantt Chart')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()

        st.pyplot(fig)

        server_2a = [nested[0] for nested in server_2]
        server_2b = [nested[1] for nested in server_2]

        fig, ax = plt.subplots(figsize=(10, 6))

        for i, (s, e) in enumerate(zip(server_2a, server_2b)):
            ax.barh(i, e - s, left=s, height=0.6, align='center', color='blue')
        
        list2 = [f'Customer {i+len(server_1a)+1}' for i in range(len(server_2a))]

        ax.set_xlabel('Time')
        ax.set_ylabel('Customers')
        ax.set_yticks(range(len(server_2a)))
        ax.set_yticklabels(list2)
        ax.set_title('Gantt Chart')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()

        st.pyplot(fig)

        total_service_time = sum(service)

        l = [item for sublist in server_1 for item in sublist]
        res1 = [*set(l)]
        server1_time = sorted(res1)

        server1_utilization = (sum([interval[1] - interval[0] for interval in server_1]) / total_service_time)/60

        m = [item for sublist in server_2 for item in sublist]
        res2 = [*set(m)]
        server2_time = sorted(res2)

        server2_utilization = (sum([interval[1] - interval[0] for interval in server_2]) / total_service_time)/60

        Total_server_utilization_rate = server1_utilization + server2_utilization

        Total_server_idle_rate = 1 - Total_server_utilization_rate
        st.text(f"Server 1 Utilization Rate: {round(server1_utilization, 2)}")

        st.text(f"Server 2 Utilization Rate: {round(server2_utilization, 2)}")

        st.text(f"Total Server Utilization Rate: {round(Total_server_utilization_rate, 2)}")
        st.text(f"Total Server Idle Rate: {round(Total_server_idle_rate, 2)}")     


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
