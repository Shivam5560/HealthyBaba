# Setup and Usage Guide

## Step 1: Install Virtual Environment
```sh
pip install virtualenv
```

## Step 2: Create and Activate Virtual Environment
```sh
virtualenv myenv
source myenv/bin/activate  # For macOS/Linux
myenv\Scripts\activate    # For Windows
```

## Step 3: Install Dependencies
```sh
pip install -r requirements.txt
```

## Step 4: Download and Install Ollama
1. Visit [Ollama](https://ollama.com) and download the appropriate version for your OS.
2. Install the application following the on-screen instructions.
3. Run the Ollama application.

## Step 5: Pull the Required Model
```sh
ollama pull qwen2.5:3b
```

## Step 6: Run the Application
```sh
python app.py
```

## Step 7: Test API Using Postman
1. Download and install [Postman](https://www.postman.com/downloads/).
2. Open Postman and create a **POST** request to:
   ```
   http://127.0.0.1:5000/generate_report
   ```
3. In the **Body** section, select **raw** and choose **JSON** format.
4. Provide the necessary JSON input.

## Example JSON Body
```json
{
  "parameter1": ["value1","value2"],
  "parameter2": ["value1","value2"]
}
```

## Notes
- Ensure that the virtual environment is activated before running `python app.py`.
- The server should be running before making the API request in Postman.
- Modify `requirements.txt` as needed for additional dependencies.

## Troubleshooting
- If you encounter issues, verify that all installations are correct and all services are running.

