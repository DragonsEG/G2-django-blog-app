# blog-application v2
Technical Documentation for a Django Blog Application

Introduction
This technical documentation outlines the architecture, features, and authentication levels for a blog application built using the Django web framework. The blog application includes the following features :

1.Users can create and publish blog posts
2. Users can view and comment on blog posts
3.Blog posts are sorted by publication date, with the most recent posts appearing first.
4.Users can create and manage categories for their blog posts.
5.Users can draft blog posts before publishing them
6.Users can edit and delete their blog posts

Additionally, the application implements various authentication levels, including viewer, writer, admin, a company with one or more than one writer, and signed user.

Architecture
Technology Stack :
- Python	
- Django Framework	
- SQLite (for data storage)	
- HTML/Bootstrap for front-end	
- JavaScript	
- Django's built-in authentication system

Features
User Authentication Levels

Viewer: Users with this level can view published blog posts and comments but cannot create or edit posts. They can also sign up for an account

Writer: Writers can create, edit, and delete their own blog posts. They can also view and comment on other posts

Admin: Admin users have full control over the blog application. They can manage user accounts, categories, and all blog posts. They can also moderate comments

Company with Writers: This level is designed for organizations or companies. It allows a company to have one or more writers under their account. Writers within a company can create, edit, and delete blog posts, but the company admin can oversee and manage all blog content created by writers in the company.

Signed User: A signed user is a registered user who has a profile but doesn't have any specific role. view and comment on others' posts


Blog Features
Create and Publish Blog Posts: Writers and company writers can create new blog posts and publish them. They can set a publication date and time for scheduling posts.

View and Comment on Blog Posts: Users can view published blog posts and leave comments on them. Comments can be moderated by admins.

Sort Posts by Publication Date: Blog posts are sorted by publication date in descending order, displaying the most recent posts first.

Create and Manage Categories: Writers and company writers can create and assign categories to their blog posts. Categories help organize and filter posts.

Draft Blog Posts: Users can save blog posts as drafts before publishing them. This feature allows writers to work on posts over time.

Edit and Delete Blog Posts: Users can edit their own blog posts and delete them if needed.



Authentication and Authorization

The authentication and authorization system is integrated with Django's built-in authentication framework. Users can register, log in, and log out. Access to specific features is controlled based on the user's authentication level.


Conclusion
This technical documentation outlines the key features and architecture of the Django blog application. The application is designed to provide a robust and flexible platform for users to create, manage, and interact with blog posts, while differentiating user capabilities through various authentication levels.
