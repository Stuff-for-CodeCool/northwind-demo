# from database import handler
from database import run_query

# @handler
# def show_all_categories(cursor):
#     query = "SELECT * FROM categories;"
#     cursor.execute(query)
#     return cursor.fetchall()
#     # return cursor.fetchone()


def show_all_categories():
    return run_query("SELECT * FROM categories;")


def get_category_details(cat_id):
    query = """
        SELECT
            category_name,
            description
        FROM categories
            WHERE category_id = %(id)s;
        """

    return run_query(
        query,
        {"id": cat_id},
        True,
    )


#     cursor.execute(query, {
#         "id": cat_id
#     })

# @handler
# def get_category_details(cursor, cat_id):
#     query = """
#         SELECT
#             category_name,
#             description
#         FROM categories
#             WHERE category_id = %(id)s;
#         """
#     cursor.execute(query, {
#         "id": cat_id
#     })
#     print(cursor.query.decode("utf-8"))
#     return cursor.fetchone()


def insert_new_category(name, desc):
    new_id = run_query(
        "SELECT max(category_id)::int AS max FROM categories;",
        single=True,
    )
    return run_query(
        """
        INSERT INTO categories (category_id, category_name, description)
        VALUES (%(id)s, %(name)s, %(desc)s)
        RETURNING category_id;
        """,
        {
            "id": int(new_id.get("max")) + 1,
            "name": name,
            "desc": desc,
        },
        single=True,
    )


def remove_category(id):
    return run_query(
        """
        DELETE FROM categories
        WHERE category_id = %(id)s
        RETURNING *;
        """,
        {"id": id},
        single=True,
    )
