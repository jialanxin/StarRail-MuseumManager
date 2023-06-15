import pandas as pd
from itertools import combinations
import numpy as np
df = pd.read_json("workerInfo.json")
new_column_names = {
    "n": "name",
    "t": "TimeContrib",
    "s": "ScienceContrib",
    "f": "PopularityContrib"
}

df = df.rename(columns=new_column_names)
nameList = df["name"]

workload1 = pd.DataFrame({"TimeContrib":[289-160],"ScienceContrib":[260-180],"PopularityContrib":[290-160]})
workload2 = pd.DataFrame({"TimeContrib":[345-190],"ScienceContrib":[308-170],"PopularityContrib":[213-180]})
workload3 = pd.DataFrame({"TimeContrib":[225-150],"ScienceContrib":[280-160],"PopularityContrib":[320-170]})




def contribution_destination(worker_group1,worker_group2,worker_group3):
    work_result_calc = lambda work_frac: np.minimum(work_frac["TimeContrib"],1)+np.minimum(work_frac["ScienceContrib"],1)+np.minimum(work_frac["PopularityContrib"],1)
    work_frac1 = worker_group1.sum()/workload1
    work_result1 = work_result_calc(work_frac1)
    work_frac2 = worker_group2.sum()/workload2
    work_result2 = work_result_calc(work_frac2)
    work_frac3 = worker_group3.sum()/workload3
    work_result3 = work_result_calc(work_frac3)
    
    return work_result1[0]+work_result2[0]+work_result3[0]


selected_rows = df.iloc[:9]
left_df = df.drop(selected_rows.index)
current_result = 0
current_group = None
best_result = 0
best_group = None
T = 2
delta_list = []
for i in range(1000):
        # random_row_df1 = selected_rows.sample(n=1)
        # random_row_df2 = left_df.sample(n=1)
        # selected_rows.loc[random_row_df1.index] = random_row_df2.values
        # left_df.loc[random_row_df2.index] = random_row_df1.values
        selected_rows = df.sample(n=9)
        worker_group1 = selected_rows.iloc[0:3]
        worker_group2 = selected_rows.iloc[3:6]
        worker_group3 = selected_rows.iloc[6:9]
        result_of_this_trial = -1*contribution_destination(worker_group1,worker_group2,worker_group3)
        Delta_E = current_result-result_of_this_trial
        delta_list.append(current_result)

        p = np.random.rand()
        if p<np.exp(Delta_E/T):
            # print(np.exp(Delta_E/1))
            current_result = result_of_this_trial
            current_group = selected_rows
        if best_result-result_of_this_trial > 0:
            best_result = result_of_this_trial
            best_group = selected_rows
        T = 0.995*T
        if i%100 ==0:
            # worker_group1 = selected_rows.iloc[0:3]
            # worker_group2 = selected_rows.iloc[3:6]
            # worker_group3 = selected_rows.iloc[6:9]
            # result_of_this_trial = -1*contribution_destination(worker_group1,worker_group2,worker_group3)
            # print(result_of_this_trial)
            print(T)
print(best_group)
# worker_group1 = best_group.iloc[0:3]
# worker_group2 = best_group.iloc[3:6]
# worker_group3 = best_group.iloc[6:9]
# work_result_calc = lambda work_frac: np.minimum(work_frac["TimeContrib"],1)+np.minimum(work_frac["ScienceContrib"],1)+np.minimum(work_frac["PopularityContrib"],1)
# work_frac1 = worker_group1.sum()/workload1
# work_result1 = work_result_calc(work_frac1)
# work_frac2 = worker_group2.sum()/workload2
# work_result2 = work_result_calc(work_frac2)
# work_frac3 = worker_group3.sum()/workload3
# work_result3 = work_result_calc(work_frac3)
# print(work_result1[0]+work_result2[0]+work_result3[0])
# # import plotly.graph_objects as go

# fig= go.Figure()
# fig.add_trace(go.Scatter(y=delta_list))
# fig.show()