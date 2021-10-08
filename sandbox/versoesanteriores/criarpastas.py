# importing os module
import os

# Parent Directory path
# parent_dir = "F:\CentralDeNotas\ClubedeBeneficios\\2021\\12\\"
parent_dir = "F:\CentralDeNotas\modelo"

months_directory_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

days_directory_list_31 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                "31"
                  ]

days_directory_list_30 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"
                  ]

days_directory_list_29 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                "21", "22", "23", "24", "25", "26", "27", "28", "29"
                  ]

for month in months_directory_list:
    print(month)
    if month == ("01", "03", "05", "07", "08", "10", "12"):
        for day in days_directory_list_31:
            path = os.path.join(parent_dir, month, day)
            os.mkdir(path)
            print("Directory '% s' created" % path)
    elif month == ("04", "06", "09", "11"):
        for day in days_directory_list_30:
            path = os.path.join(parent_dir, month, day)
            os.mkdir(path)
            print("Directory '% s' created" % path)
    else:
        for day in days_directory_list_29:
            path = os.path.join(parent_dir, month, day)
            os.mkdir(path)
            print("Directory '% s' created" % path)
