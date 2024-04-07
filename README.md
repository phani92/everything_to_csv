# Everything to CSV

* Simple script that converts pdf or xlsx file to csv file.
* Planned to extend it.

## Usage

Follow these steps to get a development environment running:

1. Create a virtual environment using the following command:
    ```
    python3 -m venv xlsxTocsv
    ```
    Note: The name `*Tocsv` for the virtual environment is already part of the `.gitignore` file.

2. Activate the virtual environment:
    - For Windows:
    ```
    .\xlsxTocsv\Scripts\activate
    ```
    - For Linux/Mac:
    ```
    source xlsxTocsv/bin/activate
    ```

3. Install the necessary packages using pip:
    ```
    pip install -r requirements.txt
    ```

4. Run script
    ```
    python main.py <input_file> <output_file>
    ```

5. (Optional) Run PyInstaller to create the executable:
    ```
    python -m PyInstaller -F xlsxTocsv.py
    ```
