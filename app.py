import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

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

def view_all_titles():
    c.execute("SELECT DISTINCT title FROM blog_table")
    data = c.fetchall()
    return data

def get_blog_by_title(title):
    c.execute('SELECT * FROM blog_table WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data

def get_blog_by_author(author):
    c.execute('SELECT * FROM blog_table WHERE author="{}"'.format(author))
    data = c.fetchall()
    return data

# Layout templates
title_temp = """
<div style="background-color:#a3a3c2;padding:10px,margin:10px; border-radius: 5px;">
    <h4 style="color:white;text-align:center;">{}</h1>
    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle; float:left; width:50px; height:50px; border-radius: 50%;">
        <h6>Author: {}</h6>
        <br/>
        <br/>
    <p style="text-align:justify">{}</[>
</div>
<br/>
"""

article_temp = """
<div style="background-color:#a3a3c2;padding:10px,margin:10px; border-radius: 5px;">
    <h4 style="color:white;text-align:center;">{}</h1>
        <h6>Author: {}</h6>
        <h6>Added on: {}</h6>
        <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle; float:left; width:50px; height:50px; border-radius: 50%;">
        <br/>
        <br/>
    <p style="text-align:justify">{}</[>
</div>
"""

head_message_temp = """
<div style="background-color:#a3a3c2;padding:10px,margin:10px; border-radius: 5px;">
    <h4 style="color:white;text-align:center;">{}</h1>
    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle; float:left; width:50px; height:50px; border-radius: 50%;">
        <h6>Author: {}</h6>
        <h6>Added on: {}</h6>
</div>

"""

full_message_temp = """
<div style="background-color:silver; overflow-x: auto; padding: 10px; border-radius: 5px; margin: 10px;
    <p style="text-align: justify; color: black; padding: 10px:>{}</p>
</div>
"""

def main():
    """
    Simple CRUD blog website using streamlit
    :return:
    """

    st.title("Blog")

    menu = ["Home","View posts","Add post","Search","Blog management"]
    choice = st.sidebar.selectbox("Menu:",menu)

    if choice == "Home":

        st.subheader("Home")

        result = view_all_posts()

        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_post = str(i[2])[0:300]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_title,b_author,b_post,b_post_date),unsafe_allow_html=True)

    elif choice == "View posts":

        st.subheader("View articles:")

        titles_list = [i[0] for i in view_all_titles()]
        posts = st.sidebar.selectbox("View posts: ",titles_list)
        post_result = get_blog_by_title(posts)
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            b_post = i[2]
            b_post_date = i[3]
            st.markdown(head_message_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)
            st.markdown(full_message_temp.format(b_post), unsafe_allow_html=True)

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

        search = st.text_input("Enter search term: ")
        search_choice = st.radio("Search by: ",("title", "author"))

        if st.button("Search"):

            if search_choice == "title":
                post_result = get_blog_by_title(search)
            elif search_choice == "author":
                post_result = get_blog_by_author(search)

            for i in post_result:
                b_author = i[0]
                b_title = i[1]
                b_post = i[2]
                b_post_date = i[3]
                st.markdown(head_message_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)
                st.markdown(full_message_temp.format(b_post), unsafe_allow_html=True)

    elif choice == "Blog management":

        st.subheader("Manage articles")

        result = view_all_posts()
        clean_db = pd.DataFrame(result, columns=["Author", "Title", "Posts", "Date"])
        st.dataframe(clean_db)


if __name__ == '__main__':
    main()