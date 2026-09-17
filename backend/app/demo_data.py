from datetime import date, timedelta

CITIES = [("Hobart","TAS"),("Launceston","TAS"),("Melbourne","VIC"),("Sydney","NSW"),("Brisbane","QLD"),("Perth","WA"),("Adelaide","SA"),("Canberra","ACT"),("Newcastle","NSW"),("Geelong","VIC")]
ROLES = [
("Data Analyst","Data & Analytics",["SQL","Python","Power BI","Git"]),
("Data Engineer","Data Engineering",["Python","SQL","ETL","AWS","Docker","Git"]),
("Machine Learning Engineer","AI & ML",["Python","Machine Learning","SQL","Docker","AWS","Git"]),
("AI Engineer","AI & ML",["Python","Artificial Intelligence","Machine Learning","REST APIs","Git"]),
("Software Developer","Software Engineering",["JavaScript","TypeScript","React","Node.js","REST APIs","Git"]),
("Backend Developer","Software Engineering",["Python","FastAPI","SQL","Docker","REST APIs","Git"]),
("Cloud Engineer","Cloud & DevOps",["AWS","Azure","Docker","Kubernetes","Terraform","CI/CD","Linux","Git"]),
("IT Support Analyst","IT Support",["IT Support","Microsoft 365","Networking","Linux","Git"]),
("Cyber Security Analyst","Cybersecurity",["Cybersecurity","Networking","Linux","Python","Git"]),
("Business Intelligence Analyst","Data & Analytics",["SQL","Power BI","Tableau","Python","Git"]),
("Platform Engineer","Cloud & DevOps",["Linux","Docker","Kubernetes","AWS","CI/CD","Terraform","Git"]),
("Java Developer","Software Engineering",["Java","SQL","REST APIs","Docker","Git"]),
]
COMPANIES=["Harbour Digital","Southern Data Lab","TasTech Solutions","Bluegum Systems","Koala Cloud","Southern Cross Analytics","Riverstone Software","Orbit Data","Coastal Networks","Civic Technology Group","Aurora Digital","Wattle AI"]
EXTRA=["Azure","GCP","Spark","Kafka","Django","C#","C++"]

def build_demo_jobs():
    jobs=[]; n=1
    for cycle in range(2):
        for i,(title,role,base) in enumerate(ROLES):
            for j in range(len(CITIES)):
                city,state=CITIES[(j+i*2+cycle)%len(CITIES)]
                graduate=(i+j+cycle)%4==0
                skills=list(dict.fromkeys(base+([EXTRA[(i+j+cycle)%len(EXTRA)]] if (i+j)%3==0 else [])))
                jobs.append({
                    "job_id":f"AU-{n:04d}",
                    "title":("Graduate "+title) if graduate else title,
                    "company":COMPANIES[(i*3+j+cycle)%len(COMPANIES)],
                    "city":city,"state":state,
                    "description":f"Join a technology team delivering {role.lower()} outcomes. The role uses {', '.join(skills)} and values practical problem solving, communication, testing and documentation.",
                    "salary":"$70k-$82k sample" if graduate else "$90k-$125k sample",
                    "employment_type":"Contract" if (i+j)%5==0 else "Full-time",
                    "role_type":role,
                    "experience_level":"Graduate" if graduate else ("Mid" if (i+j)%3==0 else "Entry"),
                    "date_posted":date(2026,9,1)+timedelta(days=(i*10+j+cycle)%15),
                    "source":"Curated portfolio demo",
                    "skills":skills,
                }); n+=1
    return jobs[:240]
