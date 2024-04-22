import psycopg2

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'


def update_versus_points(challenge_id, user_id, additional_points):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # First, determine if the user is the challenger or the challengee for this challenge
        cur.execute('''
            SELECT challenger_id, challengee_id
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return
        
        challenger_id, challengee_id = result
        
        # Depending on whether the user is the challenger or the challengee,
        # increment the corresponding points column for that user in the challenges table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges
                SET challenger_points = COALESCE(challenger_points, 0) + %s
                WHERE id = %s;
            ''', (additional_points, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_points = COALESCE(challengee_points, 0) + %s
                WHERE id = %s;
            ''', (additional_points, challenge_id))
        else:
            print("User is not part of this challenge.")
            return
        
        conn.commit()
        print("User points incremented successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
#-----------------------------------------------------------------------

def calculate_versus(distance, time):

    if time < 10 and distance < 10:
        return 1000
    else:
        distance -= 10
        if distance < 0:
            raise ValueError("Distance cannot be negative")
        dis_points = max(0, 1 - distance / 100) * 900
        if time < 0 or time > 120:
            raise ValueError("Time taken must be between 0 and the maximum allowed time")
        time_points = max(0, 1 - time / 120) * 100
        return dis_points + time_points

def get_winner(challenge_id):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT winner_id FROM matches WHERE challenge_id = %s;", (challenge_id,))
        result = cur.fetchone()
        if result is None:
            return None
        else:
            return result[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

def update_versus_pic_status(challenge_id, user_id, index):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # First, determine if the user is the challenger or the challengee for this challenge
        cur.execute('''
            SELECT challenger_id, challengee_id
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return
        
        challenger_id, challengee_id = result
        
        # Depending on whether the user is the challenger or the challengee,
        # update the corresponding finished column in the matches table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges
                SET challenger_bool[%s] = TRUE
                WHERE id = %s;
            ''', (index, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_bool[%s] = TRUE
                WHERE id = %s;
            ''', (index, challenge_id))
        else:
            print("User is not part of this challenge.")
            return
        
        conn.commit()
        print("Finish status updated successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
        
#-----------------------------------------------------------------------

def store_versus_pic_points(challenge_id, user_id, index, points):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # First, determine if the user is the challenger or the challengee for this challenge
        cur.execute('''
            SELECT challenger_id, challengee_id
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return
        
        challenger_id, challengee_id = result
        
        # Depending on whether the user is the challenger or the challengee,
        # update the corresponding finished column in the matches table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges
                SET challenger_points[%s] = %s
                WHERE id = %s;
            ''', (index, points, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_points[%s] = %s
                WHERE id = %s;
            ''', (index, points, challenge_id))
        else:
            print("User is not part of this challenge.")
            return
        
        conn.commit()
        print("Points updated successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------------------------------

def store_versus_pic_points(challenge_id, user_id, index, points):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # First, determine if the user is the challenger or the challengee for this challenge
        cur.execute('''
            SELECT challenger_id, challengee_id
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))

        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return

        challenger_id, challengee_id = result

        # Depending on whether the user is the challenger or the challengee,
        # update the corresponding points column in the challenges table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges
                SET challenger_pic_points[%s] = %s
                WHERE id = %s;
            ''', (index, points, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_pic_points[%s] = %s
                WHERE id = %s;
            ''', (index, points, challenge_id))
        else:
            print("User is not part of this challenge.")
            return

        conn.commit()
        print("Versus pic points updated successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------------------------------

def update_versus_pic_status(challenge_id, user_id, index):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # First, determine if the user is the challenger or the challengee for this challenge
        cur.execute('''
            SELECT challenger_id, challengee_id
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))

        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return

        challenger_id, challengee_id = result

        # Depending on whether the user is the challenger or the challengee,
        # update the corresponding boolean value in the challenges table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges
                SET challenger_bool[%s] = TRUE
                WHERE id = %s;
            ''', (index, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_bool[%s] = TRUE
                WHERE id = %s;
            ''', (index, challenge_id))
        else:
            print("User is not part of this challenge.")
            return

        conn.commit()
        print("Versus pic status updated successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------------------------------