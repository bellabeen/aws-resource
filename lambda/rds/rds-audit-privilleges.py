import csv
import psycopg2

# Dictionary of RDS endpoints and their corresponding credentials
rds_credentials = {
    'DB_1': {
        'user': 'username',
        'password': 'password',
        'dbname': 'namadb',
        'host': 'endpoint'
    },
    'DB_2': {
        'user': 'username',
        'password': 'password',
        'dbname': 'namadb',
        'host': 'endpoint'
    }
}

# Iterate over each RDS endpoint and its credentials
for endpoint, db_credentials in rds_credentials.items():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_credentials)
        cursor = conn.cursor()

        # Execute the query
        cursor.execute("""
            SELECT u.usename AS username,
                   tp.grantee,
                   tp.table_catalog,
                   tp.table_schema,
                   tp.table_name,
                   tp.privilege_type
            FROM (SELECT usename FROM pg_user WHERE usename NOT IN ('odoo', 'postgres')) AS u
            JOIN information_schema.table_privileges tp ON u.usename = tp.grantee
            WHERE tp.privilege_type IN ('INSERT', 'DELETE');
        """)

        # Fetch the results
        rows = cursor.fetchall()

        # Write the results to a CSV file
        with open(f"{endpoint}_permissions.csv", "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write header
            csv_writer.writerow(["Endpoint", "Username", "Grantee", "Table Catalog", "Table Schema", "Table Name", "Privilege Type"])
            # Write rows
            for row in rows:
                csv_writer.writerow([endpoint] + list(row))

        print(f"CSV file '{endpoint}_permissions.csv' created successfully.")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error connecting to {endpoint}: {e}")