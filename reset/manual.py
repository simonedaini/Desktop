import pyad.adquery
import pyad.aduser

# Configurazione della query
user = "sdaini"
q = pyad.adquery.ADQuery()
q.execute_query(
    attributes=["cn"],
    where_clause="sAMAccountName = '{}'".format(user),
    base_dn="CN=users,DC=lab,DC=com"
)            
cn = None
for row in q.get_results():
    cn = row["cn"]
password = "Changemebitch!"
ad_user = pyad.aduser.ADUser.from_cn(cn)
print(ad_user)
ad_user.set_password(password)