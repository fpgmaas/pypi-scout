import requests
import json

def get_package_list():
    url = "https://pypi.org/simple/"
    response = requests.get(url)
    package_list = response.text.split('\n')
    return package_list

def get_package_info(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    packages = get_package_list()
    print(packages[0:20])
    filtered_packages = []

    for package in packages:
        if package:
            package_info = get_package_info(package)
            if package_info:
                readme = package_info['info'].get('description', '')
                filtered_packages.append({
                    'name': package,
                    'readme': readme
                })

    # Save the filtered package data
    with open('filtered_packages.json', 'w') as f:
        json.dump(filtered_packages, f, indent=4)

if __name__ == "__main__":
    main()
