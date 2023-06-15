import pandas as pd
import numpy as np
df = pd.read_json("workerInfo copy.json")
new_column_names = {
    "n": "name",
    "t": "TimeContrib",
    "s": "ScienceContrib",
    "f": "PopularityContrib"
}

df = df.rename(columns=new_column_names)

workload1 = pd.DataFrame({"TimeContrib": [
                         375-220], "ScienceContrib": [295-190], "PopularityContrib": [460-270]})
workload2 = pd.DataFrame({"TimeContrib": [
                         460-220], "ScienceContrib": [380-220], "PopularityContrib": [280-180]})
workload3 = pd.DataFrame({"TimeContrib": [
                         280-170], "ScienceContrib": [437-230], "PopularityContrib": [400-210]})
workload4 = pd.DataFrame({"TimeContrib": [
                         365-199], "ScienceContrib": [365-231], "PopularityContrib": [346-199]})

def contribution_destination(worker_group):
    worker_group1 = worker_group.iloc[0:3]
    worker_group2 = worker_group.iloc[3:6]
    worker_group3 = worker_group.iloc[6:9]
    worker_group4 = worker_group.iloc[9:12]
    def work_result_calc(work_frac): return np.where(work_frac[["TimeContrib","ScienceContrib","PopularityContrib"]]>= 1,1,0).sum()
    work_frac1 = worker_group1.sum()/workload1
    work_result1 = work_result_calc(work_frac1)
    work_frac2 = worker_group2.sum()/workload2
    work_result2 = work_result_calc(work_frac2)
    work_frac3 = worker_group3.sum()/workload3
    work_result3 = work_result_calc(work_frac3)
    work_frac4 = worker_group4.sum()/workload4
    work_result4 = work_result_calc(work_frac4)

    return work_result1+work_result2+work_result3+work_result4



def enum_workers(df_left_upper, df_virtual_upper, nameList_upper, nest_num, total_optim, total_optim_df):
    if total_optim[1]%1000==0:
        print(total_optim)
    total_optim[1] += 1
    for (idx, worker) in df_left_upper.iterrows():
        if nest_num == 0:
            print(idx)
        nameList = nameList_upper.copy()
        nameList.append(worker["name"])
        df_left = df[~df["name"].isin(nameList)]
        df_left_max = df_left.max()
        df_virtual = df_virtual_upper.copy(deep=True)
        df_virtual.iloc[nest_num] = worker
        if nest_num == 11:
            func_up_bound = contribution_destination(df_virtual)
            if func_up_bound <= total_optim[0]:
                continue
            else:
                total_optim[0] = func_up_bound
                total_optim_df[0] = df_virtual
        else:
            for i in range(nest_num+1, 12):
                df_virtual.iloc[i] = df_left_max
            func_up_bound = contribution_destination(df_virtual)
            if func_up_bound <= total_optim[0]:
                continue
            else:
                enum_workers(df_left, df_virtual, nameList,
                             nest_num+1, total_optim, total_optim_df)


if __name__ == "__main__":
    total_optim = [0, 0]
    total_optim_df = [None]
    enum_workers(df, df.sample(n=12), [], 0, total_optim, total_optim_df)
    print(total_optim)
    print(total_optim_df[0])
