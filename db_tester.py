import pymysql

keys = [
    'sV', 'sT', 'tOL', 'pI_c', 'pI_eN', 'pI_iA_s1', 'pI_iA_s2', 'pI_iA_c', 'pI_iA_sOC', 'pI_iA_sOCD',
    'pI_iA_zC', 'pI_iPN', 'pI_jOI', 'pI_iPNL_v', 'pI_ePNL_v', 'pI_eT', 'pI_yOI_wFY', 'pI_yOI_v',
    'rPL_rPI_rPN_fN', 'rPL_rPI_rPN_lN', 'rPL_rPI_rPA_s1', 'rPL_rPI_rPA_s2', 'rPL_rPI_rPA_c', 'rPL_rPI_rPA_sOC',
    'rPL_rPI_rPA_sOCD', 'rPL_rPI_rPA_zC', 'rPL_rPI_rPRL_r', 'rPL_rPI_rC', 'rPL_rPI_rPN_fN_1',
    'rPL_rPI_rPN_lN_1', 'rPL_rPI_rPA_s1_1', 'rPL_rPI_rPA_s2_1', 'rPL_rPI_rPA_c_1', 'rPL_rPI_rPA_sOC_1',
    'rPL_rPI_rPA_sOCD_1', 'rPL_rPI_rPA_zC_1', 'rPL_rPI_rPRL_r_1', 'rPL_rPI_rC_1', 'rPL_rPI_rPN_fN_2',
    'rPL_rPI_rPN_lN_2', 'rPL_rPI_rPA_s1_2', 'rPL_rPI_rPA_s2_2', 'rPL_rPI_rPA_c_2', 'rPL_rPI_rPA_sOC_2',
    'rPL_rPI_rPA_sOCD_2', 'rPL_rPI_rPA_zC_2', 'rPL_rPI_rPRL_r_2', 'rPL_rPI_rC_2', 'rPL_rPI_rPN_fN_3',
    'rPL_rPI_rPN_lN_3', 'rPL_rPI_rPA_s1_3', 'rPL_rPI_rPA_s2_3', 'rPL_rPI_rPA_c_3', 'rPL_rPI_rPA_sOC_3',
    'rPL_rPI_rPA_sOCD_3', 'rPL_rPI_rPA_zC_3', 'rPL_rPI_rPRL_r_3', 'rPL_rPI_rC_3', 'oD_iG_iGT', 'oD_iG_iFI_iFT',
    'oD_iG_iFI_i40A', 'oD_iS_rR', 'oD_fEE_i', 'oD_fEE_i_1', 'oD_fEE_i_2', 'oD_tOF_nOA_iA', 'oD_tOF_dOFS_v',
    'oD_dOO_mTOY', 'oD_tOSO_iPIFT', 'oD_bCT_iBCT', 'oD_mIA', 'oD_sCL_r_rN', 'oD_sCL_r_rCRDN', 'oD_sCL_r_aBDN',
    'oD_sCL_r_aBDCRDN', 'oD_sCL_r_rA_s1', 'oD_sCL_r_rA_s2', 'oD_sCL_r_rA_c', 'oD_sCL_r_rA_sOC',
    'oD_sCL_r_rA_sOCD', 'oD_sCL_r_rA_zC', 'oD_sCL_r_sOSL_s', 'oD_sCL_r_sOSL_d', 'oD_sCL_r_sOSL_s_1',
    'oD_sCL_r_sOSL_d_1', 'oD_sCL_r_sOSL_s_2', 'oD_sCL_r_sOSL_d_2', 'oD_sCL_r_sOSL_s_3', 'oD_sCL_r_sOSL_d_3',
    'oD_sCL_r_sOSL_s_4', 'oD_sCL_r_sOSL_d_4', 'oD_sCL_r_sOSL_s_5', 'oD_sCL_r_sOSL_d_5', 'oD_sCL_r_sOSL_s_6',
    'oD_sCL_r_sOSL_d_6', 'oD_sCL_r_sOSL_s_7', 'oD_sCL_r_sOSL_d_7', 'oD_sCL_r_sOSL_s_8', 'oD_sCL_r_sOSL_d_8',
    'oD_sCL_r_sOSL_s_9', 'oD_sCL_r_sOSL_d_9', 'oD_sCL_r_sOSL_s_10', 'oD_sCL_r_sOSL_d_10', 'oD_sCL_r_sOSL_s_11',
    'oD_sCL_r_sOSL_d_11', 'oD_sCL_r_sOSL_s_12', 'oD_sCL_r_sOSL_d_12', 'oD_sCL_r_fS', 'oD_sCL_r_rN_1',
    'oD_sCL_r_rCRDN_1', 'oD_sCL_r_aBDN_1', 'oD_sCL_r_aBDCRDN_1', 'oD_sCL_r_rA_s1_1', 'oD_sCL_r_rA_s2_1',
    'oD_sCL_r_rA_c_1', 'oD_sCL_r_rA_sOC_1', 'oD_sCL_r_rA_sOCD_1', 'oD_sCL_r_rA_zC_1', 'oD_sCL_r_fS_1',
    'oD_oSA_tOA', 'oD_oSA_tAS', 'oD_oSA_tR', 'oD_i_hNAI', 'oD_i_tNAI', 'oD_sCFF_sC_dA', 'oD_sCFF_fF_dA',
    'oD_uOP_gPU_dA', 'oD_sB_aR', 'oD_sB_s_iN', 'oD_sB_s_sN', 'oD_sB_s_nOS', 'oD_sB_s_sT', 'oD_sB_s_sD'
]

logTxt = "Saving data into mySQL..."
print(logTxt)

# DB_HOST = '159.65.234.92'
DB_HOST = 'localhost'
DB_USER = 'root'
# DB_PASSWORD = 'bluedream'
DB_PASSWORD = 'passion1989'
DB_NAME = 'gallery'

db = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
logTxt = "Connected to the database successfully"
print(logTxt)

# prepare a cursor object using cursor() method
cur = db.cursor()

sql = "DROP TABLE IF EXISTS Total_first"
cur.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS Total_first(ID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL, "

sub_sql = "%s TEXT, " * len(keys)
sub_sql = sub_sql[:-2]

sql = sql + sub_sql + ")"
sql = sql % tuple(keys)
cur.execute(sql)
db.commit()

select_sql = "SELECT * FROM Total_first"
cur.execute(select_sql)

if cur.fetchone():
    print("OK")
else:
    print("Bad")


