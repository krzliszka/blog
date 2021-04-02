import streamlit as st
import sqlite3

conn = sqlite3.connect('blog.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blog_table('
              'author MESSAGE_TEXT,'
              'title MESSAGE_TEXT,'
              'article MESSAGE_TEXT,'
              'post_date DATE)')

def add_data(author,title,article,post_date):
    c.execute('INSERT INTO blog_table(author, title, article, post_date)'
              'VALUES (?,?,?,?)',(author,title,article,post_date))
    conn.commit()

def view_all_posts():
    c.execute('SELECT * FROM blog_table')
    data = c.fetchall()
    return data

def main():
    """
    Simple CRUD blog website using streamlit
    :return:
    """

    st.title("Blog")

    menu = ["Home","View posts","Add post","Search","Blog management"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")

        result = view_all_posts()
        st.write(result)

    elif choice == "View posts":
        st.subheader("View articles:")

    elif choice == "Add post":
        st.subheader("Add articles:")

        create_table()

        blog_author = st.text_input("Enter author name:",max_chars=50)
        blog_title = st.text_input("Enter post title:")
        blog_article = st.text_area("Write your article here:")
        blog_post_date = st.date_input("Date: ")

        if st.button("Add"):
            add_data(blog_author,blog_title,blog_article,blog_post_date)
            st.success("Post:{} saved".format(blog_title))

    elif choice == "Search":
        st.subheader("Search articles:")

    elif choice == "Blog management":
        st.subheader("Manage articles:")


if __name__ == '__main__':
    main()