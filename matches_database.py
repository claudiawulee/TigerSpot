import psycopg2

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'


#dont run again
def create_matches_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER,
    winner_id VARCHAR(255),
    challenger_score INTEGER,
    challengee_score INTEGER);''')
    conn.commit()
    cur.close()
    conn.close()
    
#-----------------------------------------------------------------------

def clear_matches_table():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Deletes all records from the matches table
        cur.execute("DELETE FROM matches;")
        conn.commit()  # Commit the transaction to make changes permanent
        print("Matches table cleared.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error clearing matches table: {error}")
    finally:
        if conn is not None:
            conn.close()

            
# Complete a match
def complete_match(challenge_id, winner_id, challenger_score, challengee_score):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("UPDATE challenges SET status = 'completed' WHERE id = %s;", (challenge_id,))
        cur.execute("INSERT INTO matches (challenge_id, winner_id, challenger_score, challengee_score) VALUES (%s, %s, %s, %s) RETURNING id;", (challenge_id, winner_id, challenger_score, challengee_score))
        match_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print(f"Match completed with ID: {match_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def main():
    #clear_matches_table()
    print()
    
if __name__=="__main__":
    main()