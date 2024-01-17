import csv
import os

def calculate_scores(path):
    if path is not None:
        if os.path.exists(path):
            with open(path, 'r') as file:
                reader = csv.reader(file)
                student_data = {} 
                
                for row in reader:
                # Assuming row[0] is the student's ID, row[1] is the name, 
                # and row[2] onwards are the scores
                    student_id = row[0]
                    name = row[1]
                    scores = [int(score) for score in row[2:]] 

                # Store the data in the dictionary
                    student_data[student_id] = {"name": name, "scores": scores}

                # TODO: Further processing, like calculating averages
                
        else:
            print("Path doesn't exist.")
    else:
        print("No path has been provided.")
        
calculate_scores("path/to/your/csvfile.csv")