# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:38:20 2019

@author: aprabhakar
"""
import pandas as pd

dfREMS_Apollo = pd.read_csv(r"C:\Users\aprabhakar\Desktop\snakes\CVStuff\testImages\LiveRems.csv", converters={i: str for i in range(100)})



# This function loads a pandas dataframe from a CSV file without trying to
# assign the data specific types (just strings [or 'objects' in dataframe parlance])
def read_csv_as_strings(url):
    print(f"Getting data from {url}...")
    # print(pd.read_csv(url, converters={i: str for i in range(100)}))
    return pd.read_csv(url, converters={i: str for i in range(100)})


# The 4 FDA REMS data files are located at these addresses we'll loop through
csvurls = [r'https://www.accessdata.fda.gov/scripts/cder/rems/index.cfm?event=csvAllRems.page',
           r'https://www.accessdata.fda.gov/scripts/cder/rems/index.cfm?event=csvMaterials.page',
           r'https://www.accessdata.fda.gov/scripts/cder/rems/index.cfm?event=csvModification.page',
           r'https://www.accessdata.fda.gov/scripts/cder/rems/index.cfm?event=csvRemsProduct.page']

# When downloaded, the corresponding file names are here.  Doris and Inna refer to these
# datasets using these names, so we'll use those
csvfns = ["REMS", "REMS_Materials", "REMS_Versions", "REMS_Products"]

# Using "df" + filename as the dataframe name for the file
dfnames = ["df" + fn for fn in csvfns]

# This creates the dataframes as "global variables" -- for viewing them in Spyder
# globals() was the only way I could figure out how to fill a "variable" variable
# name -- not recommended, but to explore, it works.
for i in range(0, len(dfnames)):
    globals()[dfnames[i]] = read_csv_as_strings(csvurls[i])

dfREMS_Active = dfREMS.loc[dfREMS["Inactive_Flag"] == "No"]

dfBothDrugNames = pd.read_csv(r"C:\Users\aprabhakar\Desktop\Access DB - Like SDI\dfREMS_Active_Apollo_Compare.csv")

#Inner joins and selecting required columns to get a table containing Description(Apollo Drug Names), Risk ID , REMSID
temp = dfREMS_Active[['REMSID','Drug Name']]
dfNamesAndREMSID = pd.merge(temp,dfBothDrugNames, how='inner',left_on = 'Drug Name', right_on = 'From_Website')
temp = dfREMS_Apollo[['Risk ID','Description']]
dfNameAndRiskIDAndREMSID = pd.merge(temp,dfNamesAndREMSID, how='inner', left_on = 'Description', right_on = 'From_Apollo')[['Description','Risk ID','REMSID']]

#Replacing the ` with nothing in Application_Number in dfREMS_Products (Application Number is from Website, Not Apollo)
dfREMS_Products["Application_Number"] = dfREMS_Products["Application_Number"].apply(lambda x:(x.replace("`","")))
dfREMSIDAndApplicationNumber = pd.merge(dfNameAndRiskIDAndREMSID,dfREMS_Products, how = 'inner',left_on = 'REMSID', right_on = 'REMSID')[['Description','Risk ID','REMSID','Application_Number']]

#(Application Number is from Apollo)
dfNDCAndRISK_ID = pd.read_excel(r"C:\Users\aprabhakar\Desktop\Access DB - Like SDI\RHRMNDL0_NDC_RISK_LINK.xlsx")
dfNDCAndAPPL_NO = pd.read_excel(r"C:\Users\aprabhakar\Desktop\Access DB - Like SDI\RAPPLNA0_FDA_NDC_APPL.xlsx")
dfRISK_IDAndAPPL_NO = pd.merge(dfNDCAndRISK_ID,dfNDCAndAPPL_NO, how = 'inner',left_on = 'NDC', right_on = 'NDC')[['RISK_ID','APPL_NO']]
dfRISK_IDAndAPPL_NO = dfRISK_IDAndAPPL_NO.astype(str)


dfApolloAppNumberAndWebAppNumber = pd.merge(dfREMSIDAndApplicationNumber,dfRISK_IDAndAPPL_NO, how = 'inner',left_on = 'Risk ID', right_on = 'RISK_ID')



# After running the above, you should have close to the following:
# dfREMS =            284 rows, 5 columns   ['REMSID', 'Drug Name', 'REMS Shared System ', 'Website', 'Inactive_Flag']
# dfREMS_Materials = 4221 rows, 7 columns   ['REMSID', 'REMS_Name', 'Version_ID', 'Version_Date', 'Material_ID', 'Material_Name', 'Material_Link']
# dfREMS_Versions =  1022 rows, 17 columns   ['REMSID', 'REMS_Name', 'VersionID', 'Version_Date', 'Released_Flag', 'Moved_to_Shared_System_Flag', 'Medication_Guide_Flag', 'Communication_Plan_Flag', 'Elements_to_Assure_Safe_Use_Flag', 'Implementation_System_Flag', 'Prescriber_Certification_Flag', 'Dispenser_Certification_Flag', 'Patient_Enrollment_Flag', 'Prescriber_Training_Flag', 'Revision_Flag', 'Current_Approved_Flag', 'REMS_Goals']
# dfREMS_Products =   807 rows, 12 columns   ['REMSID', 'REMS_Name', 'Established_Name', 'Trade_Name', 'Dosage_Form', 'Application_Type', 'Application_Number', 'Added_Date', 'Approval_Date', 'Withdrawal_Date', 'Label_Link', 'Drugs at FDA Link']


# EXTRAS we'll talk about later --

# The "primary keys" corresponding to each file -- only one record per combination
# of these values should exist

# csvunx = [["REMSID"],
#          ["REMSID","Version_ID","Material_ID"],
#          ["REMSID","VersionID"],
#          ["REMSID","Application_Number","Dosage_Form"]]

# df.set_index(unique_index_columns_lst, drop=False, inplace=True, verify_integrity=True)
    

#df_sdi = pd.read_excel(r"C:\Users\aprabhakar\Desktop\Access DB - Like SDI\qryActiveREMsDrugs.xlsx")
#df_sdi['RISK_ID'] = df_sdi['RISK_ID'].apply(str)
#set(df_sdi['RISK_ID'].to_list()) - set(dfREMS_Apollo['Risk ID'].to_list())
#set(dfREMS_Apollo['Risk ID'].to_list()) - set(df_sdi['RISK_ID'].to_list()) 

#def tolower(s):
#   return s.lower()

# df_sdi['lcdesc'] = df_sdi['RISK_GRP_DESC'].apply(tolower)

# dfREMS_ID_Relations = pd.DataFrame(columns = ['Risk ID', 'REMSID', 'Drug Name'])

#count = 0
#for index, row in dfREMS_Active.iterrows():
#    REMS_DrugName = row["Drug Name"]
#    for index, row in dfREMS_Apollo.iterrows():
#        Apollo_DrugName = row['Description']
#        Apollo_DrugName = re.findall('\w+',row['Description'])[0]
#        print(Apollo_DrugName)
#    break
#        if REMS_DrugName.lower() == Apollo_DrugName.lower():
#            print(REMS_DrugName.lower())
#            count += 1
#        Partial_Ratio = fuzz.partial_ratio(REMS_DrugName.lower(),Apollo_DrugName.lower())
#        if Partial_Ratio > 80:
#            print(REMS_DrugName)
#            count += 1
        


 



