#-----------------------------------------------------------------------
# matches_database.py
#-----------------------------------------------------------------------

import psycopg2

#-----------------------------------------------------------------------

DATABASE_URL = 'postgresql://tigerspot_database_990e_user:s5cZDU5NrHEaLniMWf2C4L2kzOIxigFZ@dpg-cruv9ig8fa8c73cobdog-a.ohio-postgres.render.com/tigerspot_database_990e'
# DATABASE_URL = 'postgresql://tigerspot_database_user:uzR6eRWos4EgeX39bk3kAY7akdrfmV2O@dpg-cre8kjbgbbvc73bos7v0-a.ohio-postgres.render.com/tigerspot_database'

#-----------------------------------------------------------------------

# Create matches table
def create_matches_table():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS matches (
                id SERIAL PRIMARY KEY,
                challenge_id INTEGER,
                winner_id VARCHAR(255),
                challenger_score INTEGER,
                challengee_score INTEGER);''')
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error clearing matches table: {error}")
        return "database error"

#-----------------------------------------------------------------------
# Clear the matches table
def clear_matches_table():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Deletes all records from the matches table
                cur.execute("DELETE FROM matches;")
                conn.commit()  # Commit the transaction to make changes permanent
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error clearing matches table: {error}")
        return "database error"

#-----------------------------------------------------------------------

# Complete a match
def complete_match(challenge_id, winner_id, challenger_score, challengee_score):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE challenges SET status = 'completed' WHERE id = %s;", (challenge_id,))
                cur.execute("INSERT INTO matches (challenge_id, winner_id, challenger_score, challengee_score) VALUES (%s, %s, %s, %s) RETURNING id;", (challenge_id, winner_id, challenger_score, challengee_score))
                conn.commit()
                return "success"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def main():
    
    # Testing
    print('Testing')
    create_matches_table()
    # complete_match('1', '123', 1000, 500)
    # clear_matches_table()

#-----------------------------------------------------------------------

if __name__=="__main__":
    main()