import os
import xml.etree.ElementTree as ET
from collections import defaultdict

def check_duplicates_in_file(file_path, dbid_counts, file_dbids):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for elem in root.iter():
            if elem.tag == 'dbid':
                dbid = elem.text
                dbid_counts[dbid] += 1
                file_dbids[file_path].append(dbid)
    except ET.ParseError:
        print(f"Error parsing XML file: {file_path}")
        exit(1)

def main():
    dbid_counts = defaultdict(int)
    file_dbids = defaultdict(list)

    xml_files = ['data/protomods.xml', 'data/techtreemods.xml']

    for file_path in xml_files:
        if os.path.exists(file_path):
            check_duplicates_in_file(file_path, dbid_counts, file_dbids)

    duplicates = {dbid: count for dbid, count in dbid_counts.items() if count > 1}

    if duplicates:
        for dbid, count in duplicates.items():
            print(f"DBID {dbid} appears {count} times")
            print("Found in files:")
            for file_path, dbids in file_dbids.items():
                if dbid in dbids:
                    print(f"- {file_path}")
        exit(1)
    else:
        print("No duplicates found")
        exit(0)

if __name__ == "__main__":
    main()
