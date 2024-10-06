```python
import psycopg2
import pandas as pd
import multiprocessing as mp



# Number of rows per chunk
CHUNK_SIZE = 10

# Number of parallel processes
NUM_PROCESSES = 4

# CSV file output directory
OUTPUT_DIR = r'C:\temp\diskCache'

# CSV compression format ('gzip', 'zip', None)
COMPRESSION = 'zip'

LOCAL_CONNECTION_STRING = "postgresql://postgres:admin@localhost:5432/test"
TABLE_NAME = 'student'
def get_db_connection():
    """
    Function to establish a connection to the PostgreSQL database.
    """
    return psycopg2.connect(
        LOCAL_CONNECTION_STRING
    )


def export_chunk(start_row, chunk_size, output_dir, compression, file_num):
    """
    Function to export a chunk of data from PostgreSQL to CSV.
    """
    # Establish connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Prepare the query to fetch a chunk of data
    query = f"SELECT * FROM {TABLE_NAME} OFFSET {start_row} LIMIT {chunk_size};"
    cursor.execute(query)

    # Fetch the rows
    rows = cursor.fetchall()

    # Get column names from the cursor
    colnames = [desc[0] for desc in cursor.description]

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(rows, columns=colnames)

    # Define the output file name based on the chunk
    output_file = f"{output_dir}/output_part_{file_num}.zip"

    # Write the chunk to a CSV file with optional compression
    df.to_csv(output_file, index=False)

    # Close the database connection
    cursor.close()
    conn.close()

    print(f"Chunk {file_num} written to {output_file}")


def main():
    # Establish connection to get the total number of rows
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the total number of rows in the table
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
    total_rows = cursor.fetchone()[0]

    # Close the connection
    cursor.close()
    conn.close()

    # Generate start rows for each chunk
    chunk_starts = [(i, CHUNK_SIZE, OUTPUT_DIR, COMPRESSION, file_num)
                    for file_num, i in enumerate(range(0, total_rows, CHUNK_SIZE))]

    # Use multiprocessing to export chunks in parallel
    with mp.Pool(processes=NUM_PROCESSES) as pool:
        pool.starmap(export_chunk, chunk_starts)

    print("All chunks exported.")


if __name__ == "__main__":
    main()


```