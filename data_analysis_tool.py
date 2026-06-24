import subprocess
import os
import json

class Tools:
    @staticmethod
    async def log_to_excel(
        file_path: str, __event_emitter__=None
    ) -> str:
        """
        Convert a log file to structured Excel format with summary statistics.
        Use this when a user uploads a .log file and wants it in Excel format.
        
        :param file_path: Full path to the log file
        :return: Path to the generated Excel file
        """
        try:
            result = subprocess.run(
                ['python', 'D:/stage1/tools/data_tool.py', 'log', file_path],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                output_path = result.stdout.strip().replace('Log converted to: ', '')
                return f"SUCCESS: Log file converted to Excel at: {output_path}"
            else:
                return f"ERROR: {result.stderr}"
        except Exception as e:
            return f"ERROR converting log: {str(e)}"
    
    @staticmethod
    async def excel_eda(
        file_path: str, __event_emitter__=None
    ) -> str:
        """
        Perform full Exploratory Data Analysis on an Excel/CSV file.
        Generates a comprehensive Excel output with:
        - Original data
        - Column information (types, missing values, unique counts)
        - Descriptive statistics for numeric columns
        - Cleaned data (missing values filled, duplicates removed)
        - Outlier detection with IQR method
        - Value counts for categorical columns
        - Overall summary sheet
        
        Use this when a user uploads Excel/CSV data and wants analysis, cleaning, or EDA.
        
        :param file_path: Full path to the Excel or CSV file
        :return: Path to the generated EDA Excel file
        """
        try:
            result = subprocess.run(
                ['python', 'D:/stage1/tools/data_tool.py', 'eda', file_path],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                output_path = result.stdout.strip().replace('EDA completed: ', '')
                return f"SUCCESS: Full EDA completed! Output file at: {output_path}\n\nThe output Excel contains multiple sheets: Original data, Column Info, Statistics, Cleaned Data, Outlier Detection, Value Counts, and Overall Summary."
            else:
                return f"ERROR: {result.stderr}"
        except Exception as e:
            return f"ERROR performing EDA: {str(e)}"
    
    @staticmethod
    async def get_output_files(
        __event_emitter__=None
    ) -> str:
        """
        List all generated output files from log conversion and EDA.
        Use this when a user wants to see what output files are available.
        
        :return: List of output files with paths
        """
        try:
            output_dir = "D:/stage1/output"
            if not os.path.exists(output_dir):
                return "No output files found. Output directory doesn't exist yet."
            
            files = os.listdir(output_dir)
            if not files:
                return "No output files found. The output directory is empty."
            
            result = "Available output files:\n\n"
            for f in sorted(files):
                full_path = os.path.join(output_dir, f)
                size_kb = os.path.getsize(full_path) / 1024
                result += f"- {f} ({size_kb:.1f} KB)\n  Path: {full_path}\n\n"
            
            return result
        except Exception as e:
            return f"ERROR listing files: {str(e)}"