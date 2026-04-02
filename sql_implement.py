import pandas as pd
from sqlalchemy import create_engine, text
USER     = "root"        
PASSWORD = "your_password_here" 
HOST     = "localhost"
PORT     = "3306"
DB       = "your_database_name_here"
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")
try:
    with engine.connect() as conn:
        print("Connected successfully")
except Exception as e:
    print("Connection failed:", e)
df = pd.read_csv("clean_jobs.csv")
skill_cols = ["python","sql","aws","docker","kubernetes",
              "spark","java","pytorch","tensorflow","go"]

#Build dimension dataframes
companies = df[["company"]].drop_duplicates().dropna().reset_index(drop=True)
companies["company_id"] = companies.index + 1

locations = df[["location"]].drop_duplicates().dropna().reset_index(drop=True)
locations["location_id"] = locations.index + 1

#Create tables with proper PKs first
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS jobs"))
    conn.execute(text("DROP TABLE IF EXISTS companies"))
    conn.execute(text("DROP TABLE IF EXISTS locations"))

    conn.execute(text("""
        CREATE TABLE companies (
            company_id INT PRIMARY KEY,
            company    VARCHAR(255)
        )
    """))

    conn.execute(text("""
        CREATE TABLE locations (
            location_id INT PRIMARY KEY,
            location    VARCHAR(255)
        )
    """))

    conn.execute(text(f"""
        CREATE TABLE jobs (
            job_id           INT PRIMARY KEY AUTO_INCREMENT,
            title            VARCHAR(255),
            role_category    VARCHAR(100),
            company_id       INT,
            location_id      INT,
            salary_min       FLOAT,
            salary_max       FLOAT,
            avg_salary       FLOAT,
            salary_predicted TINYINT,
            contract_time    VARCHAR(50),
            created          DATETIME,
            {", ".join(f"`{s}` TINYINT" for s in skill_cols)},
            FOREIGN KEY (company_id)  REFERENCES companies(company_id),
            FOREIGN KEY (location_id) REFERENCES locations(location_id)
        )
    """))
    conn.commit()
    print("Tables created with primary keys")
#Load data
companies.to_sql("companies", engine, if_exists="append", index=False)
print(f"companies: {len(companies)} rows")

locations.to_sql("locations", engine, if_exists="append", index=False)
print(f"locations: {len(locations)} rows")

df_jobs = df.merge(companies, on="company", how="left") \
            .merge(locations, on="location", how="left")

jobs_table = df_jobs[[
    "title", "role_category", "company_id", "location_id",
    "salary_min", "salary_max", "avg_salary", "salary_predicted",
    "contract_time", "created", *skill_cols
]]
jobs_table.to_sql("jobs", engine, if_exists="append", index=False)
print(f"jobs: {len(jobs_table)} rows")

print("\n Database ready")