#Assuming all these fields exist and remain unchanged.
# index = 0
# key = []
# for data in dict_all:
#     key.append((dict_all[index]['package_size_code'],
#     dict_all[index]['fda_ther_equiv_code'], 
#     dict_all[index]['fda_application_number'],
#     dict_all[index]['clotting_factor_indicator'],
#     dict_all[index]['year'],
#     dict_all[index]['fda_product_name'],
#     dict_all[index]['labeler_name'],
#     dict_all[index]['ndc'],
#     dict_all[index]['product_code'],
#     dict_all[index]['unit_type'],
#     dict_all[index]['fda_approval_date'],
#     dict_all[index]['market_date'],
#     dict_all[index]['pediatric_indicator'],
#     dict_all[index]['package_size_intro_date'],
#     dict_all[index]['units_per_pkg_size'],
#     dict_all[index]['labeler_code'],
#     dict_all[index]['desi_indicator'],
#     dict_all[index]['drug_category'],
#     dict_all[index]['quarter'],
#     dict_all[index]['cod_status']))
#     index = index + 1


    #c.execute("INSERT INTO dregs VALUES (60,'NR',204153,'N',2018,'LUZU Cream 1% 60gm','MEDICIS DERMATOLOGICS, INC.',99207085060, 0850,'GM','2013-11-14T00:00:00','2014-03-14T00:00:00','N','2014-03-14T00:00:00',60000, 99207,1,'S',2,3)")
#c.executemany("INSERT INTO drugs2 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", result)





# Deletes all entries from a table.
# sql = 'DELETE from drugs2'
# c.execute(sql)

#Print all entries in a table
# c.execute('''SELECT * FROM drugs''')
# for row in c:
#         print(row)