import pyad.adquery
import pyad.aduser

q = pyad.adquery.ADQuery()

q.execute_query(
    attributes=["cn"],
    where_clause="sAMAccountName = 'sdaini'",
    base_dn="CN=users,DC=lab,DC=com"
)

cn = None
for row in q.get_results():
    cn = row["cn"]
        

ad_user = pyad.aduser.ADUser.from_cn(cn)
try:
    ad_user.set_password("Bubiman10!!")
    print("password Aggiornata")
except Exception as e:
    print(e)