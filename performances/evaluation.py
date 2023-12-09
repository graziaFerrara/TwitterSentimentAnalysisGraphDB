import matplotlib.pyplot as plt
import pandas as pd

# Complex queries data
complex_queries = pd.read_csv('performances/complex_queries_performances.csv')
complex_queries_gdb = pd.read_csv('performances/complex_queries_performances_GDB.csv')

# Combine the data for plotting
merged_data = pd.merge(complex_queries, complex_queries_gdb, on='operation')
merged_data.columns = ['operation', 'time_mongodb', 'time_neo4j']

# Plotting
plt.figure(figsize=(10, 6))

bar_width = 0.35
index = merged_data.index

plt.barh(index, merged_data['time_mongodb'], bar_width, label='MongoDB', color='red')
plt.barh(index + bar_width, merged_data['time_neo4j'], bar_width, label='Neo4j', color='blue')

plt.xlabel('Time (s)')
plt.ylabel('Operation')
plt.title('Complex Queries Performances')
plt.yticks(index + bar_width / 2, merged_data['operation'])
plt.legend()

plt.tight_layout()

# save the plot
plt.savefig('performances/complex_queries_performances.png')

# do the same for other queries

# Simple queries data
simple_queries = pd.read_csv('performances/other_queries_performances.csv')
simple_queries_gdb = pd.read_csv('performances/other_queries_performances_GDB.csv')

# Combine the data for plotting
merged_data = pd.merge(simple_queries, simple_queries_gdb, on='operation')
merged_data.columns = ['operation', 'time_mongodb', 'time_neo4j']

# Plotting
plt.figure(figsize=(10, 6))

bar_width = 0.35
index = merged_data.index

plt.barh(index, merged_data['time_mongodb'], bar_width, label='MongoDB', color='red')
plt.barh(index + bar_width, merged_data['time_neo4j'], bar_width, label='Neo4j', color='blue')

plt.xlabel('Time (s)')
plt.ylabel('Operation')
plt.title('Other Queries Performances')
plt.yticks(index + bar_width / 2, merged_data['operation'])
plt.legend()

plt.tight_layout()

# save the plot
plt.savefig('performances/other_queries_performances.png')

