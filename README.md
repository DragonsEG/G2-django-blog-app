# Blog_App_G2_Team
Version-1 of Blog App with Auth and Permissions.
Title: Simple Blog Application with Django

Introduction:
The following document outlines the design and features of a simple blog application built using Django. The application allows users to create and publish blog posts, view and comment on existing posts, and provides different authentication levels for users: viewer, writer, and admin.

1. Application Overview:
The blog application is designed to provide a platform where users can share their thoughts and engage with other users through blog posts and comments. The core features of the application include post creation, publishing, viewing, and commenting.

2. User Authentication Levels:
The application supports three authentication levels:

a) Viewer: Viewers have the ability to browse and read blog posts. They can view published posts, comments. However, they cannot create or publish their own posts or comments.

b) Writer: Writers have all the privileges of viewers and can additionally create, edit, and publish their own blog posts. They can also delete their own posts .

c) Admin: Admin users have all the privileges of writers and can additionally manage all blog posts and comments on the site. They have the authority to delete or modify any post or comment, regardless of the user who created it.

3. Blog Post Functionality:
The application provides the following features related to blog posts:

a) Create and Publish Posts: Writers and admins can create new blog posts using a user-friendly interface. They can add a title, content the post. Once created, they can publish the post, making it visible to viewers.

b) View Posts: Viewers, writers, and admins can browse and read published blog posts. Posts are displayed in a sorted order based on their publication date, with the most recent posts appearing first. Each post includes the title, content, author, publication date.

c) Edit and Delete Posts: Writers and admins have the ability to edit or delete their own posts. This functionality allows them to update the content, modify tags, or remove posts that are no longer relevant.

4. Comment Functionality:
The application provides the following features related to comments:

a) Comment on Posts: Viewers, writers, and admins can leave comments on published blog posts to share their thoughts or engage in discussions. Comments are displayed below the respective blog post and include the commenter's name, date, and content.



5. Security and Permissions:
To ensure security and prevent unauthorized access, the application implements appropriate authentication and authorization mechanisms. User authentication is required to access the blog application, and different levels of access are granted based on the user's role.

Conclusion:
The simple blog application developed using Django provides a user-friendly platform for creating, publishing, and interacting with blog posts. It supports different authentication levels, allowing users to have varying levels of access and privileges. By incorporating features such as post creation, publication, viewing, commenting, and appropriate security measures, the application aims to enhance the user experience and encourage engagement within the blogging community.
