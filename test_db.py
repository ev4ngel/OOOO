import axdb,os
db=axdb.axDB(os.path.join(os.getcwd(),"wangwei"))

print db.getPages()
