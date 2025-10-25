UK Crime Blog with Interactive Heatmap and Admin Analytics

A Flask-based web application that visualizes crime hotspots across South Wales using real-world data and Folium heatmaps. The platform includes a blog system with posts, comments, and Bootstrap styling for a polished user experience. Recent updates introduce admin analytics, contributor tracking, and enhanced user interface elements.

Features

•	Interactive Folium heatmap of crime data
•	Blog posts with comment functionality
•	Contributor leaderboard with post and comment counts
•	Emoji reaction system with usage analytics chart
•	Inactive user detection based on last activity
•	SQLite database powered by SQLAlchemy
•	Bootstrap-integrated UI for responsive design
•	Dynamic routing and post previews
•	Visible login, logout, and register buttons on homepage
•	Admin dashboard with filters, stats, charts, and blog post management
•	AI-powered crime summaries and blog insights 

Dataset

Crime data sourced from the UK Police API and filtered for South Wales between 2022 and 2025.

How to Run

1.	Clone the repository
2.	Create and activate a virtual environment
3.	Install dependencies:
pip install -r requirements.txt
4  Run database migrations:
    flask db upgrade
5  Start the application:
	flask run
6  Access the site at: http://127.0.0.1:5000

Environment Configuration

The application uses environment variables for runtime configuration. These should be defined in a .env file or set directly in the deployment environment.
Required variables:
	FLASK_ENV=production
    SECRET_KEY=your-secret-key
    DATABASE_URL=your-database-url

To load these variables locally, the application uses python-dotenv.

Deployment

This project is configured for deployment on Railway using Gunicorn.

Deployment files:

•	requirements.txt: Lists all Python dependencies
•	Procfile: Specifies the web process (web: gunicorn app:create_app())
•	runtime.txt: Defines the Python version (e.g. python-3.10.12)
•	.env: Contains environment-specific configuration

Deployment steps:

•  Push the project to a GitHub repository
1.	Connect the repository to Railway
2.	Set required environment variables in Railway
3.	Provision a PostgreSQL database if needed
4.	Trigger deployment from the Railway dashboard

Database Migrations

Database schema changes are managed using Flask-Migrate.

To initialize migrations:
	flask db init

To generate a migration:
flask db migrate -m "Initial migration"

To apply migrations:
	flask db upgrade

Future Enhancements

•	Filter heatmap by crime type or year
•	Embedded maps within blog posts
•	Comment moderation and like system
•	Reaction analytics by post, user, and time
•	Search and filter functionality for posts and users
•	Admin panel for user management and post moderation
•	CI/CD pipeline with GitHub Actions
•	Custom domain and SSL configuration

Testing

Basic testing can be performed using Flask’s built-in test client. Unit tests for routes, models, and forms can be added using pytest or unittest.
Contributing
Contributions are welcome. Please fork the repository and submit a pull request with clear documentation and test coverage.

License

This project is licensed under the MIT License.

Author

Hassan Devx
Full-stack developer focused on data-driven dashboards, scalable web apps, and AI-powered analytics.
GitHub: github.com/HassanDevx








