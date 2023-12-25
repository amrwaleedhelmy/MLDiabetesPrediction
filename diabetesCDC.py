import pandas as pd
import numpy as np

# Read the XPT file into a DataFrame

document = {}

column_mapping = {
    'SEQN': 'Respondent sequence number',
}


def readFile(year):
    dfGLU = pd.read_sas(str(year) + "-" + str(year+1) + "/GLU.XPT")
    dfGHB = pd.read_sas(str(year) + "-" + str(year+1) + "/GHB.XPT")
    dfDIQ = pd.read_sas(str(year) + "-" + str(year+1) + "/DIQ.XPT")
    dfDBQ = pd.read_sas(str(year) + "-" + str(year+1) + "/DBQ.XPT")
    dfBPX = pd.read_sas(str(year) + "-" + str(year+1) + "/BPX.XPT")
    dfMCQ = pd.read_sas(str(year) + "-" + str(year+1) + "/MCQ.XPT")
    dfPAQ = pd.read_sas(str(year) + "-" + str(year+1) + "/PAQ.XPT")
    dfBPQ = pd.read_sas(str(year) + "-" + str(year+1) + "/BPQ.XPT")
    dfBMX = pd.read_sas(str(year) + "-" + str(year+1) + "/BMX.XPT")
    dfDEMO = pd.read_sas(str(year) + "-" + str(year+1) + "/DEMO.XPT")
    dfR1TOT = pd.read_sas(str(year) + "-" + str(year+1) + "/DR1TOT.XPT")

    merged_df = pd.merge(dfGLU, dfGHB, on='SEQN')
    merged_df1 = pd.merge(merged_df, dfDIQ, on='SEQN')
    merged_df2 = pd.merge(merged_df1, dfDBQ, on='SEQN')
    merged_df2 = pd.merge(merged_df2, dfR1TOT, on='SEQN')
    merged_df2 = pd.merge(merged_df2, dfDEMO, on='SEQN')
    merged_df2 = pd.merge(merged_df2, dfBPX, on='SEQN')
    merged_df2 = pd.merge(merged_df2, dfMCQ, on='SEQN')
    merged_df2 = pd.merge(merged_df2, dfPAQ, on='SEQN')
    merged_df2 = pd.merge(merged_df2, dfBMX, on='SEQN')
    merged_df2 = pd.merge(merged_df2, dfBPQ, on='SEQN')
    if year == 2017:
        merged_df2.rename(columns={"DR1TWSZ": "DR1TWS"}, inplace=True)

    def calculateAge(row):
        if row["RIDAGEYR"] >= 60:
            return (row["Score"] + 3)
        elif row["RIDAGEYR"] >= 50:
            return (row["Score"] + 2) 
        elif row["RIDAGEYR"] >= 40:
            return (row["Score"] + 1) 
        if row["RIAGENDR"] == 1:
            return (row["Score"] + 1)
        
    def calculateFamily(row):
        if row["MCQ300C"] == 1:
            return (row["Score"] + 1)
        
    def calculateActivity(row):
        if row["PAQ605"] == 0:
            if row["PAQ620"] == 0:
                if row["PAQ650"] == 0:
                    if row["PAQ665"] == 0:
                        if row["PAQ635"] == 0:
                            return (row["Score"] + 1)
                        else:
                            return 0
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    
    def calculateBMI(row):
        if row["BMXBMI"] >= 40:
            return (row["Score"] + 3)
        elif row["BMXBMI"] >= 30:
            return (row["Score"] + 2)
        elif row["BMXBMI"] >= 25:
            return (row["Score"] + 1)

    def calculateScore(row):
        return (row["Age"] + row["Family"] + row["Activity"] + row["BMI"])


    merged_df2["Score"] = 0
    merged_df2["Age"] = 0
    merged_df2["Family"] = 0
    merged_df2["Activity"] = 0
    merged_df2["BMI"] = 0

    merged_df2["Age"] = merged_df2.apply(calculateAge, axis=1)
    merged_df2["Family"] = merged_df2.apply(calculateFamily, axis=1)
    merged_df2["Activity"] = merged_df2.apply(calculateActivity, axis=1)
    merged_df2["BMI"] = merged_df2.apply(calculateBMI, axis=1)
    merged_df2["Score"] = merged_df2.apply(calculateScore, axis=1)

    merged_df2 = merged_df2[(merged_df2['DIQ010'] != 1)
                            & (merged_df2['DIQ160'] != 1)]
    merged_df2["Has Diabetes"] = np.where(
        ((merged_df2['LBXGLU'] >= 126) | (merged_df2['LBXGH'] >= 6.5)), "True", "False")
    merged_df2["CDC Questionnaire"] = np.where((merged_df2['Score'] >= 5), "True", "False")
    merged_df2 = merged_df2[["Has Diabetes", "Age", "Family", "Activity", "BMI", "Score", "CDC Questionnaire"]]
    limitPer = len(merged_df2) * .6
    merged_df2 = merged_df2.dropna(thresh=limitPer, axis=1)
    merged_df2.fillna(merged_df2.median(
        numeric_only=True).round(1), inplace=True)
    merged_df2 = merged_df2.drop(
        merged_df2[merged_df2['Has Diabetes'].eq("False")].sample(frac=.94599).index)
    merged_df2 = merged_df2.groupby("Has Diabetes", group_keys=False).apply(lambda x:x.sample(frac=0.3))
    document[str(year)] = merged_df2
    merged_df2.to_csv(str(year) + "-" + str(year+1) +
                      "/diabetesCDC.csv", index=False)


readFile(2011)
readFile(2013)
readFile(2015)
readFile(2017)

for x in ["2011", "2013", "2015"]:
    document[str(int(x)+2)] = pd.concat([document[x], document[str(int(x)+2)]])

document["2017"].to_csv("diabetesCDC.csv", index=False, float_format='%.4f')
