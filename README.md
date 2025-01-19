# Steps to Run the Application

Follow these steps to set up and run the application on your local machine:

1. **Download the Project**: Clone the repository or download the ZIP file from GitHub. Extract the files to your desired directory (e.g., Desktop).  

2. **Set Up the Database**: Locate the `database.txt` file in the project directory, which contains the SQL commands to create the necessary tables. Use your preferred PostgreSQL client to create the database and run the commands from `database.txt`.  

3. **Configure the Database URL**: Open the `app.py` file in a text editor and update the `SQLALCHEMY_DATABASE_URI` variable with your PostgreSQL connection URL:  
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@<host>:<port>/<database_name>'
   ```  
   Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your actual database credentials.  

4. **Create and Activate a Virtual Environment**: Create a virtual environment by running:  
   ```bash
   python -m venv venv
   ```  
   Activate the virtual environment:  
   - **Windows**:  
     ```bash
     venv\Scripts\activate
     ```  
   - **Mac/Linux**:  
     ```bash
     source venv/bin/activate
     ```  

5. **Install Dependencies**: Install the required Python packages using:  
   ```bash
   pip install -r requirements.txt
   ```  

6. **Run the Application**: Start the application by running:  
   ```bash
   python main.py
   ```  

7. **Access the Application**: Open your browser and navigate to:  
   ```
   http://127.0.0.1:5000
   ```

### Notes:
- Ensure PostgreSQL is installed and running on your machine.  
- The default configuration assumes the database is hosted locally. Adjust settings if using a remote server.  
- For further customization, refer to the project documentation or contact the maintainer.
