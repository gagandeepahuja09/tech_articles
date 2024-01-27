import csv
import requests

def check_liveness(url):
    try:
        response = requests.head(url, timeout=5)
        return 200 <= response.status_code < 400
    except requests.RequestException:
        return False

def liveness_check_bulk(input_csv, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        writer.writerow(["URL", "Status"])

        next(reader)  
        for row in reader:
            if not row:
                writer.writerow(["", "Empty"])
                continue
            
            url = row[0]
            is_alive = check_liveness(url)
            status = "Alive" if is_alive else "Not Alive"

            writer.writerow([url, status])

liveness_check_bulk("/Users/gagandeep.ahuja/Downloads/result_1943087_2024334.csv", 
"/Users/gagandeep.ahuja/Downloads/output_url_1.csv")
