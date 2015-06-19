load data 
infile 'modifier_w_clob.csv' "str '\r\n'"
append
into table BLUEHERONMETADATA.RXNORM_UNMC
fields terminated by ','
OPTIONALLY ENCLOSED BY '"' AND '"'
trailing nullcols
           ( C_HLEVEL CHAR(4000),
             C_FULLNAME CHAR(4000),
             C_NAME CHAR(4000),
             C_SYNONYM_CD CHAR(4000),
             C_VISUALATTRIBUTES CHAR(4000),
             C_BASECODE CHAR(4000),
             C_METADATAXML CHAR(4000),
             C_FACTTABLECOLUMN CHAR(4000),
             C_TABLENAME CHAR(4000),
             C_COLUMNNAME CHAR(4000),
             C_COLUMNDATATYPE CHAR(4000),
             C_OPERATOR CHAR(4000),
             C_DIMCODE CHAR(4000),
             C_TOOLTIP CHAR(4000),
             M_APPLIED_PATH CHAR(4000),
             UPDATE_DATE "sysdate",
             SOURCESYSTEM_CD CHAR(4000),
             C_NAME_ORIG CHAR(4000)
           )
