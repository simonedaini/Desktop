import pyad.adquery
import pyad.aduser

# Configurazione della query
user = "sdaini"
q = pyad.adquery.ADQuery()
q.execute_query(
    attributes=["cn", "DistinguishedName", "UserPrincipalName"],
    base_dn="CN=users,DC=lab,DC=com"
)

# Iterazione sugli utenti trovati
for row in q.get_results():
    if row["UserPrincipalName"] is not None and "@" in row["UserPrincipalName"]:
        print(row)