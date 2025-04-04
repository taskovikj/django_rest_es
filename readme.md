
# Django Blog Platform with Elasticsearch Integration

This platform empowers users to create, manage, and explore blog posts effortlessly. With features like user authentication, a custom front page, social interactions, comments, and Elasticsearch-powered search, it offers a rich and engaging experience for both bloggers and readers.

## Table of Contents
- [Starting](#starting)
- [Features](#features)
- [Testing](#testing)
- [Project Architecture](#project-architecture)
- [Usage](#usage)
- [Conclusion](#conclusion)


## Starting
### 1.1 Installation on Docker

```bash
git clone https://github.com/taskovikj/django_rest_es.git
```
```bash
docker-compose up -d --build
```

### 1.2 Wait for build
### 1.3 Load the database fixture

```bash
docker exec -it django sh
```
```bash
python manage.py loaddata dump.json
```
### 1.4 Build Elasticsearch indexes
```bash
docker exec -it django sh
```
```bash
python manage.py search_index --rebuild
```


## Features

### Authentication and Authorization

- **User Registration**: New users can easily register.
- **User Authentication**: Registered users can log in securely.
- **User Roles**: Different roles ensure proper authorization. For instance, only authenticated users can create, edit, or delete their posts.

### Custom Front Page

- **Personalized Content**: Users are greeted with a personalized front page. It showcases featured posts and content from authors they follow.

### Blog Posts

- **Create, Edit, and Delete**: Authenticated users can create, edit, and delete their blog posts.
- **Rich Content**: Blog posts include a title, content, tags, and a publication date.
- **Scheduled Posts**: Posts can be scheduled for future publication, enhancing content planning.

### Follow/Unfollow Authors

- **Social Interaction**: Users can follow or unfollow authors whose content interests them.
- **Curated Feed**: The front page displays posts from followed authors.

### Comments

- **Engagement**: Users can engage with posts by leaving comments.
- **Moderation**: Users have control over their comments, with the ability to edit or delete them.
- **Owner Permissions**: Post owners can also moderate comments on their posts.

### Email Notifications

- **Stay Informed**: Users receive email notifications for:
  - Comments on their posts.
  - Gaining new followers.
  - New posts from authors they follow.

### Elasticsearch Integration

- **Efficient Search**: Elasticsearch powers the search functionality, enabling users to find posts swiftly.
- **Search by Keywords, Tags, Authors**: Users can search for posts using keywords, tags, or author names.

## Testing

## GitHub Actions Setup

Our project leverages GitHub Actions, a CI/CD (Continuous Integration/Continuous Deployment) platform provided by GitHub, to automate various tasks, including testing.
Workflow Configuration

Our project includes a GitHub Actions workflow defined in the .github/workflows directory. The primary workflow for testing is configured to run whenever a pull request is created or updated, and for pushes to the main branch.


## Selenium Tests in Docker Standalone Container
Our Selenium tests are designed to run in a Docker standalone container, ensuring consistent test execution environments. This approach simplifies the setup process and makes it easier to run tests locally or in CI/CD pipelines.

## Instructions
### 1.1 Prepare container

```bash
docker pull selenium/standalone-chrome
```
```bash
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
```
### Docker must be already running on port 8000 
```bash
docker exec -it django sh
```
### 1.2 Run seleniuim tests
```bash
python selenium_test.py
```
### 1.3 Unit tests can also be run at this point
```bash
python manage.py test
```


## Project Architecture

Our project leverages the Django web framework and the Django Rest Framework (DRF) to build RESTful APIs. Elasticsearch is integrated for efficient content indexing and searching. Here's an overview of the components:

- **Django REST API**:

- **Elasticsearch**: Elasticsearch efficiently indexes and searches blog posts. A custom Elasticsearch indexing service keeps the data in sync with the database.

- **Frontend**: The frontend, developed using HTML, CSS, and JavaScript, communicates with the REST API to present blog posts, comments, user profiles, and manages user interactions.

- **Authentication**: Django's built-in authentication system ensures user registration, login, and logout. Token-based authentication is commonly employed for API endpoints.

- **Email Notifications**: An email notification system is configured using Django's built-in email capabilities. This system sends emails for comment notifications, new followers, and post publications.

## Usage

### User Registration and Authentication

New users can register and authenticate to access the platform.

### Creating Blog Posts

Authenticated users can create, edit, and delete their blog posts.

### Follow/Unfollow Authors

Users can follow and unfollow authors to tailor their content feed.

### Comments

Users can leave comments on blog posts and manage their comments if allowed by the post owner.

### Email Notifications

Users will receive email notifications for various events, enhancing their engagement.

### Searching for Posts

Users can utilize the Elasticsearch-powered search to find posts using keywords, tags, or authors.



## Conclusion

This project delivers a feature-rich blog platform with Elasticsearch integration to ensure efficient content search and indexing. It includes user authentication, personalized front pages, social interactions, comments, and email notifications to enhance the user experience. Whether you're a blogger or a reader, our platform aims to provide an engaging and seamless experience for all.




