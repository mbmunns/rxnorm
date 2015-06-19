load data 
infile 'rxnorm2.csv' "str '\n'"
truncate
into table RXNORM_METADATA
fields terminated by '|'
OPTIONALLY ENCLOSED BY '"' AND '"'
trailing nullcols
           ( C_HLEVEL CHAR(4000),
             C_FULLNAME CHAR(4000),
             C_NAME CHAR(4000),
             C_VISUALATTRIBUTES CHAR(4000),
             C_BASECODE CHAR(4000)
           )
