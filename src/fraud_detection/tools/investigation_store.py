
import sqlite3
from datetime import datetime

def initialize_db():
    conn = sqlite3.connect("company_investigations.db")
    cursor = conn.cursor() # object used to run SQL queries


    
# Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            directors TEXT,
            address TEXT,
            jurisdiction TEXT,
            risk_score INTEGER,
            investigation_status TEXT,
            investigated_at TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database and table created successfully.")




def save_investigation(
    company_name: str,
    directors: list[str],
    address: str,
    jurisdiction: str,
    risk_score: int,
    investigation_status: str
):
    conn = sqlite3.connect("company_investigations.db")
    cursor = conn.cursor()

    # Check for duplicate company
    cursor.execute(
        "SELECT id FROM company_investigations WHERE company_name = ?",
        (company_name,)
    )

    if cursor.fetchone():
        print(f"{company_name} already exists in the database.")
        conn.close()
        return

    directors_string = ", ".join(directors)

    investigated_at = datetime.now()

    cursor.execute("""
        INSERT INTO company_investigations (
            company_name,
            directors,
            address,
            jurisdiction,
            risk_score,
            investigation_status,
            investigated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        company_name,
        directors_string,
        address,
        jurisdiction,
        risk_score,
        investigation_status,
        investigated_at
    ))

    conn.commit()
    conn.close()

    print("Investigation saved successfully.")


def find_connections(company_name:str , directors: list[str], address: str):

    conn = sqlite3.connect("company_investigations.db")
    cursor = conn.cursor()

    matches = []

    cursor.execute("""
        select company_name , risk_score
        from company_investigations
        where address = ?  AND company_name != ? 
        """,
        (address,company_name,))

    
    for company_name, risk_score in cursor.fetchall():
        matches.append({
            "company_name": company_name,
            "matched_field": "address",
            "matched_value" : address,
            "risk_score": risk_score
        })


    
    for director in directors:
        cursor.execute("""
            select company_name, risk_score
            FROM company_investigations
            WHERE directors LIKE ? AND company_name != ? 
        """, (f"%{director}%", company_name,))

        for company_name, risk_score in cursor.fetchall():
            matches.append({
                "company_name": company_name,
                "matched_field": f"director: {director}",
                "risk_score": risk_score
            })

    conn.close()

    return matches


