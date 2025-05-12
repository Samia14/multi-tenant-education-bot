"""Store and retrive images from postgress."""
import psycopg2
from pathlib import Path
def store_images_in_podtgress(path:str)->None:
    """Store images along in postgress db."""

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="HelloWorld1!",
        host="localhost",  # or your server
        port="5432"
    )
    cur = conn.cursor()

    # Read image as binary
    folder = Path(path)

    for file in folder.iterdir():
        if file.is_file():
            with file.open("rb",encoding="utf-8") as f:
                content = f.read()
                cur.execute("INSERT INTO image.img (name, data) VALUES (%s, %s)", (file.name, psycopg2.Binary(content)))
                conn.commit()

    cur.close()
    conn.close()
    print("Image inserted successfully.")

# Example usage
store_images_in_podtgress("C:\\Users\\mysel\\Pictures\\Screenshots\\Physics\\Book9_2")