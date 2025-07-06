import platform

def print_schedule_instructions():
    os_name = platform.system().lower()
    if os_name == 'windows':
        print('To schedule drift checks, use Task Scheduler. Example:')
        print('schtasks /Create /SC DAILY /TN "ConfigDrift" /TR "python -m configdrift detect" /ST 09:00')
    elif os_name == 'linux' or os_name == 'darwin':
        print('To schedule drift checks, use cron. Example:')
        print('(crontab -e)')
        print('0 9 * * * python3 -m configdrift detect')
    else:
        print('Refer to your OS documentation for scheduling tasks.') 