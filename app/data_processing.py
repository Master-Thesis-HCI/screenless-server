from dataclasses import dataclass
import re


@dataclass
class AppData:
    name: str = None
    package_name: str = None
    time_: int = None
    total: int = 0
    type_: int = 0
    system: bool = False
    count: int = 0

def parse_android_data(android_data: str) -> list:
    result = list()
    # get chars between brackets using regex
    apps = re.match('\[(.* ?)\]', android_data).group(1).split(',')
    for app in apps:
        app_data = AppData()

        match_name = re.findall(r'name:(.*?) package_name:', app)
        if match_name:
            app_data.name = match_name[0]

        match_package_name = re.findall(r'package_name:(.*?) ', app)
        if match_package_name:
            app_data.package_name = match_package_name[0]

        match_time = re.findall(r'time:(\d*?) ', app)
        if match_time:
            app_data.time_ = int(match_time[0]) #/ 100  # use s instead of ms

        match_total = re.findall(r'total:(\d*?) ', app)
        if match_total:
            app_data.total = int(match_total[0]) #/ 100  # use s instead of ms

        match_type = re.findall(r'type:(\d*?) ', app)
        if match_type:
            app_data.type_ = int(match_type[0])

        match_system = re.findall(r'system:(.*?) ', app)
        if match_system:
            app_data.system = True if match_system[0] == 'true' else False

        match_count = re.findall(r'count:(\d*?) ', app)
        if match_count:
            app_data.count = int(match_count[0])
        result.append(app_data)
    return result


def debug():
    x = '[name:Mint Launcher package_name:com.mi.android.go.globallauncher time:1635370016299 total:9504053 type:0 system:false count:25, name:Chrome package_name:com.android.chrome time:1635354235624 total:3729888 type:0 system:false count:4, name:Camera package_name:com.android.camera time:1635352907159 total:31604 type:0 system:false count:2, name:Google Play Store package_name:com.android.vending time:1635337968473 total:19109 type:0 system:false count:2, name:Google Go package_name:com.google.android.apps.searchlite time:1635352571825 total:3497 type:0 system:false count:0, name:Calendar package_name:com.google.android.calendar time:1635352513294 total:1654 type:0 system:false count:0, name:Photos package_name:com.google.android.apps.photos time:1635352575421 total:948 type:0 system:false count:0]'
    data = parse_android_data(x)
    for d in data:
        print(d)

debug()
