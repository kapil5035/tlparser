import argparse
import datetime
import re

def tlparse(tl_file):
    with open(tl_file, encoding ="UTF-8") as f:
        #all_lines = f.readlines()
        all_lines = f.read().splitlines()

    time_log_flag = False
    total_work_time_seconds = 0

    time_log_pattern = 'Time Log'
    work_date_pattern = '[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}'
    work_times_pattern = '\d{1,2}:\d{1,2}[ap]m\s+-\s+\d{1,2}:\d{1,2}[ap]m'

    for index, line in enumerate(all_lines):
        print("Line #%d: %s" %(index+1, line))

        if (not time_log_flag):
            time_log_found = re.match(time_log_pattern, line, re.IGNORECASE)
            if time_log_found:
                time_log_flag = True
                print(f"Time Log Found: {time_log_found}\n")
            else:
                print(f"Ignoring Line {index+1}: {line}\n")
        else:
            work_date_found = re.search(work_date_pattern, line, re.IGNORECASE)
            work_times_found = re.search(work_times_pattern, line, re.IGNORECASE)

            #print("Work Date Found: ", work_date_found)
            #print("Work Times Found: ", work_times_found)

            if work_date_found and work_times_found:
                work_start_date_str = work_date_found.group(0)
                previous_work_date_str = work_start_date_str
            elif work_times_found and (not work_date_found):
                work_start_date_str = previous_work_date_str

            print("work start date: ", work_start_date_str)
            print("work start date length: ", len(work_start_date_str))

            if work_times_found:
                work_times_str = work_times_found.group(0)
                print(work_times_str)
                work_times = work_times_str.upper().split("-")
                work_start_time_str = work_times[0].strip()
                work_end_time_str = work_times[1].strip()

                work_start_time_of_day = work_start_time_str[-2:].upper()
                work_end_time_of_day = work_end_time_str[-2:].upper()

                if (work_start_time_of_day == "PM") and (work_end_time_of_day == "AM"):
                    if (len(work_start_date_str.split("/")[-1]) == 2):
                        work_end_date = datetime.datetime.strptime(work_start_date_str, '%m/%d/%y') + datetime.timedelta(days=1)
                        work_end_date_str = work_end_date.strftime('%m/%d/%y')
                    elif (len(work_start_date_str.split("/")[-1]) == 4):
                        work_end_date = datetime.datetime.strptime(work_start_date_str,'%m/%d/%Y') + datetime.timedelta(days=1)
                        work_end_date_str = work_end_date.strftime('%m/%d/%Y')
                else:
                    work_end_date_str = work_start_date_str


                work_start_date_time_str = work_start_date_str + " " + work_start_time_str
                work_end_date_time_str = work_end_date_str + " " + work_end_time_str
                print(f"Start Date Time: {work_start_date_time_str} End Date Time: {work_end_date_time_str}")

                if (len(work_start_date_str.split("/")[-1]) == 2):
                    work_start_datetime_obj = datetime.datetime.strptime(work_start_date_time_str, '%m/%d/%y %I:%M%p')
                    work_end_datetime_obj = datetime.datetime.strptime(work_end_date_time_str, '%m/%d/%y %I:%M%p')
                elif (len(work_start_date_str.split("/")[-1]) == 4):
                    work_start_datetime_obj = datetime.datetime.strptime(work_start_date_time_str, '%m/%d/%Y %I:%M%p')
                    work_end_datetime_obj = datetime.datetime.strptime(work_end_date_time_str, '%m/%d/%Y %I:%M%p')

                work_time = work_end_datetime_obj - work_start_datetime_obj
                work_time_seconds = work_time.total_seconds()
                total_work_time_seconds += work_time_seconds

                print(f"Work Time Minutes: {work_time_seconds/60}")
                print(f"Total Work Time Minutes: {total_work_time_seconds/60} \n")
            else:
                print(f"Ignoring Line #{index+1}: {line}\n")

    print(f"Total Work Time: {int(total_work_time_seconds)} Seconds")
    total_work_time = datetime.timedelta(seconds=total_work_time_seconds)
    print("Total Work Time: ", total_work_time)

    total_work_time_mins, total_work_time_secs = divmod(total_work_time_seconds, 60)
    total_work_time_hours, total_work_time_mins = divmod(total_work_time_mins, 60)

    return (total_work_time_hours, total_work_time_mins)

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("time_log_file", help="Time Log File")

    args = parser.parse_args()
    time_log_file = args.time_log_file

    total_work_time_hours, total_work_time_mins = tlparse(time_log_file)
    print(f"Total Work Time: {int(total_work_time_hours)} Hours and {int(total_work_time_mins)} Minutes")