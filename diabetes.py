import pandas as pd
import numpy as np

# Read the XPT file into a DataFrame

document = {}

column_mapping = {
    'SEQN': 'Respondent sequence number',
    'DBQ095Z': 'Type of table salt used',
    'DBD100': 'How often add salt to food at table',
    'DRQSPREP': 'Salt used in preparation?',
    'DRQSDIET': 'On special diet?',
    'DRQSDT91': 'Other special diet',
    'DR1TNUMF': 'Number of foods/beverages reported',
    'DR1TKCAL': 'Energy (kcal)',
    'DR1TPROT': 'Protein (gm)',
    'DR1TCARB': 'Carbohydrate (gm)',
    'DR1TSUGR': 'Total sugars (gm)',
    'DR1TFIBE': 'Dietary fiber (gm)',
    'DR1TTFAT': 'Total fat (gm)',
    'DR1TSFAT': 'Total saturated fatty acids (gm)',
    'DR1TMFAT': 'Total monounsaturated fatty acids (gm)',
    'DR1TPFAT': 'Total polyunsaturated fatty acids (gm)',
    'DR1TCHOL': 'Cholesterol (mg)',
    'DR1TATOC': 'Vitamin E as alpha-tocopherol (mg)',
    'DR1TATOA': 'Added alpha-tocopherol (Vitamin E) (mg)',
    'DR1TRET': 'Retinol (mcg)',
    'DR1TVARA': 'Vitamin A, RAE (mcg)',
    'DR1TACAR': 'Alpha-carotene (mcg)',
    'DR1TBCAR': 'Beta-carotene (mcg)',
    'DR1TCRYP': 'Beta-cryptoxanthin (mcg)',
    'DR1TLYCO': 'Lycopene (mcg)',
    'DR1TLZ': 'Lutein + zeaxanthin (mcg)',
    'DR1TVB1': 'Thiamin (Vitamin B1) (mg)',
    'DR1TVB2': 'Riboflavin (Vitamin B2) (mg)',
    'DR1TNIAC': 'Niacin (mg)',
    'DR1TVB6': 'Vitamin B6 (mg)',
    'DR1TFOLA': 'Total folate (mcg)',
    'DR1TFA': 'Folic acid (mcg)',
    'DR1TFF': 'Food folate (mcg)',
    'DR1TFDFE': 'Folate, DFE (mcg)',
    'DR1TCHL': 'Total choline (mg)',
    'DR1TVB12': 'Vitamin B12 (mcg)',
    'DR1TB12A': 'Added vitamin B12 (mcg)',
    'DR1TVC': 'Vitamin C (mg)',
    'DR1TVD': 'Vitamin D (D2 + D3) (mcg)',
    'DR1TVK': 'Vitamin K (mcg)',
    'DR1TCALC': 'Calcium (mg)',
    'DR1TPHOS': 'Phosphorus (mg)',
    'DR1TMAGN': 'Magnesium (mg)',
    'DR1TIRON': 'Iron (mg)',
    'DR1TZINC': 'Zinc (mg)',
    'DR1TCOPP': 'Copper (mg)',
    'DR1TSODI': 'Sodium (mg)',
    'DR1TPOTA': 'Potassium (mg)',
    'DR1TSELE': 'Selenium (mcg)',
    'DR1TCAFF': 'Caffeine (mg)',
    'DR1TTHEO': 'Theobromine (mg)',
    'DR1TALCO': 'Alcohol (gm)',
    'DR1TMOIS': 'Moisture (gm)',
    'DR1TS040': 'SFA 4:0 (Butanoic) (gm)',
    'DR1TS060': 'SFA 6:0 (Hexanoic) (gm)',
    'DR1TS080': 'SFA 8:0 (Octanoic) (gm)',
    'DR1TS100': 'SFA 10:0 (Decanoic) (gm)',
    'DR1TS120': 'SFA 12:0 (Dodecanoic) (gm)',
    'DR1TS140': 'SFA 14:0 (Tetradecanoic) (gm)',
    'DR1TS160': 'SFA 16:0 (Hexadecanoic) (gm)',
    'DR1TS180': 'SFA 18:0 (Octadecanoic) (gm)',
    'DR1TM161': 'MFA 16:1 (Hexadecenoic) (gm)',
    'DR1TM181': 'MFA 18:1 (Octadecenoic) (gm)',
    'DR1TM201': 'MFA 20:1 (Eicosenoic) (gm)',
    'DR1TM221': 'MFA 22:1 (Docosenoic) (gm)',
    'DR1TP182': 'PFA 18:2 (Octadecadienoic) (gm)',
    'DR1TP183': 'PFA 18:3 (Octadecatrienoic) (gm)',
    'DR1TP184': 'PFA 18:4 (Octadecatetraenoic) (gm)',
    'DR1TP204': 'PFA 20:4 (Eicosatetraenoic) (gm)',
    'DR1TP205': 'PFA 20:5 (Eicosapentaenoic) (gm)',
    'DR1TP225': 'PFA 22:5 (Docosapentaenoic) (gm)',
    'DR1TP226': 'PFA 22:6 (Docosahexaenoic) (gm)',
    'DR1_300': 'Compare food consumed yesterday to usual',
    'DR1_320Z': 'Total plain water drank yesterday (gm)',
    'DR1_330Z': 'Total tap water drank yesterday (gm)',
    'DR1BWATZ': 'Total bottled water drank yesterday (gm)',
    'DR1TWS': 'Tap water source',
    'DBQ010': 'Ever breastfed or fed breastmilk',
    'DBD030': 'Age stopped breastfeeding(days)',
    'DBD041': 'Age first fed formula(days)',
    'DBD050': 'Age stopped receiving formula(days)',
    'DBD055': 'Age started other food/beverage',
    'DBD061': 'Age first fed milk(days)',
    'DBQ073A': 'Type of milk first fed - whole milk',
    'DBQ073B': 'Type of milk first fed - 2% milk',
    'DBQ073C': 'Type of milk first fed - 1% milk',
    'DBQ073D': 'Type of milk first fed - fat free milk',
    'DBQ073E': 'Type of milk first fed - soy milk',
    'DBQ073U': 'Type of milk first fed - other',
    'DBQ700': 'How healthy is the diet',
    'DBQ197': 'Past 30 day milk product consumption',
    'DBQ223A': 'You drink whole or regular milk',
    'DBQ223B': 'You drink 2% fat milk',
    'DBQ223C': 'You drink 1% fat milk',
    'DBQ223D': 'You drink fat free/skim milk',
    'DBQ223E': 'You drink soy milk',
    'DBQ223U': 'You drink another type of milk',
    'DBQ229': 'Regular milk use 5 times per week',
    'DBQ235A': 'How often drank milk age 5-12',
    'DBQ235B': 'How often drank milk age 13-17',
    'DBQ235C': 'How often drank milk age 18-35',
    'DBQ301': 'Community/Government meals delivered',
    'DBQ330': 'Eat meals at Community/Senior center',
    'DBQ360': 'Attend kindergarten thru high school',
    'DBD381': '# of times/week get school lunch',
    'DBQ390': 'School lunch free, reduced or full price',
    'DBQ400': 'School serve complete breakfast each day',
    'DBD411': '# of times/week get school breakfast',
    'DBD895': '# of meals not home prepared',
    'DBD900': '# of meals from fast food or pizza place',
    'DBD905': '# of ready-to-eat foods in past 30 days',
    'DBD910': '# of frozen meals/pizza in past 30 days'
}


def readFile(year):
    dfGLU = pd.read_sas(str(year) + "-" + str(year+1) + "/GLU.XPT")
    dfGHB = pd.read_sas(str(year) + "-" + str(year+1) + "/GHB.XPT")
    dfDIQ = pd.read_sas(str(year) + "-" + str(year+1) + "/DIQ.XPT")
    dfDBQ = pd.read_sas(str(year) + "-" + str(year+1) + "/DBQ.XPT")
    dfR1TOT = pd.read_sas(str(year) + "-" + str(year+1) + "/DR1TOT.XPT")

    merged_df = pd.merge(dfGLU, dfGHB, on='SEQN')
    merged_df1 = pd.merge(merged_df, dfDIQ, on='SEQN')
    merged_df2 = pd.merge(merged_df1, dfDBQ, on='SEQN')
    merged_df2 = pd.merge(merged_df2, dfR1TOT, on='SEQN')

    if year == 2017:
        merged_df2.rename(columns={"DR1TWSZ": "DR1TWS"}, inplace=True)

    def map_diet(row):
        if row["DRQSDT1"] == 1:
            return "Weight loss diet"
        elif row["DRQSDT2"] == 2:
            return "Low fat/low cholesterol diet"
        elif row["DRQSDT3"] == 3:
            return "Low salt/Low sodium diet"
        elif row["DRQSDT4"] == 4:
            return "Sugar free/Low sugar diet"
        elif row["DRQSDT5"] == 5:
            return "Low fiber diet"
        elif row["DRQSDT6"] == 6:
            return "High fiber diet"
        elif row["DRQSDT7"] == 7:
            return "Diabetic diet"
        elif row["DRQSDT8"] == 8:
            return "Weight gain/Muscle building diet"
        elif row["DRQSDT9"] == 9:
            return "Low carbohydrate diet"
        elif row["DRQSDT10"] == 10:
            return "High protein diet"
        elif row["DRQSDT11"] == 11:
            return "Gluten-free/Celiac diet"
        elif row["DRQSDT12"] == 12:
            return "Renal/Kidney diet"
        elif row["DRQSDT91"] == 91:
            return "Other special diet"
        else:
            return "No Special Diet"

    merged_df2["DRQSDIET"] = merged_df2.apply(map_diet, axis=1)

    merged_df2 = merged_df2[(merged_df2['DIQ010'] != 1)
                            & (merged_df2['DIQ160'] != 1)]
    merged_df2["Has Diabetes"] = np.where(
        ((merged_df2['LBXGLU'] >= 126) | (merged_df2['LBXGH'] >= 6.5)), "True", "False")
    merged_df2 = merged_df2[["Has Diabetes", "DBQ095Z", "DBD100", "DRQSPREP", "DRQSDIET", "DR1TNUMF", "DR1TKCAL", "DR1TPROT", "DR1TCARB", "DR1TSUGR", "DR1TFIBE", "DR1TTFAT", "DR1TSFAT", "DR1TMFAT", "DR1TPFAT", "DR1TCHOL", "DR1TATOC", "DR1TATOA", "DR1TRET", "DR1TVARA", "DR1TACAR", "DR1TBCAR", "DR1TCRYP", "DR1TLYCO", "DR1TLZ", "DR1TVB1", "DR1TVB2", "DR1TNIAC", "DR1TVB6", "DR1TFOLA", "DR1TFA", "DR1TFF", "DR1TFDFE", "DR1TCHL", "DR1TVB12", "DR1TB12A", "DR1TVC", "DR1TVD", "DR1TVK", "DR1TCALC", "DR1TPHOS", "DR1TMAGN", "DR1TIRON", "DR1TZINC", "DR1TCOPP", "DR1TSODI", "DR1TPOTA", "DR1TSELE", "DR1TCAFF", "DR1TTHEO", "DR1TALCO", "DR1TMOIS", "DR1TS040",
                             "DR1TS060", "DR1TS080", "DR1TS100", "DR1TS120", "DR1TS140", "DR1TS160", "DR1TS180", "DR1TM161", "DR1TM181", "DR1TM201", "DR1TM221", "DR1TP182", "DR1TP183", "DR1TP184", "DR1TP204", "DR1TP205", "DR1TP225", "DR1TP226", "DR1_300", "DR1_320Z", "DR1_330Z", "DR1BWATZ", "DR1TWS", "DBQ010", "DBD030", "DBD041", "DBD050", "DBD055", "DBD061", "DBQ073A", "DBQ073B", "DBQ073C", "DBQ073D", "DBQ073E", "DBQ073U", "DBQ700", "DBQ197", "DBQ223A", "DBQ223B", "DBQ223C", "DBQ223D", "DBQ223E", "DBQ223U", "DBQ229", "DBQ235A", "DBQ235B", "DBQ235C", "DBQ301", "DBQ330", "DBQ360", "DBD381", "DBQ390", "DBQ400", "DBD411", "DBD895", "DBD900", "DBD905", "DBD910"]]
    merged_df2.rename(columns=column_mapping, inplace=True)
    limitPer = len(merged_df2) * .6
    merged_df2 = merged_df2.dropna(thresh=limitPer, axis=1)
    merged_df2 = merged_df2.drop(
        merged_df2[merged_df2['Has Diabetes'].eq("False")].sample(frac=.87).index)
    merged_df2.fillna(merged_df2.median(
        numeric_only=True).round(1), inplace=True)
    merged_df2 = merged_df2[["Has Diabetes", "How healthy is the diet", "# of meals from fast food or pizza place", "Total fat (gm)", "Beta-cryptoxanthin (mcg)", "Folic acid (mcg)", "Food folate (mcg)", "Calcium (mg)", "Caffeine (mg)", "Vitamin B12 (mcg)", "Carbohydrate (gm)", "Beta-carotene (mcg)", "Alpha-carotene (mcg)", "Energy (kcal)", "SFA 12:0 (Dodecanoic) (gm)", "Copper (mg)", "Vitamin E as alpha-tocopherol (mg)", "# of meals not home prepared", "# of frozen meals/pizza in past 30 days"]]
    document[str(year)] = merged_df2
    merged_df2.to_csv(str(year) + "-" + str(year+1) +
                      "/diabetes.csv", index=False)


readFile(2011)
readFile(2013)
readFile(2015)
readFile(2017)

for x in ["2011", "2013", "2015"]:
    document[str(int(x)+2)] = pd.concat([document[x], document[str(int(x)+2)]])

document["2017"].to_csv("diabetes.csv", index=False, float_format='%.4f')
