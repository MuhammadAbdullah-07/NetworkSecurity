from setuptools import find_packages,setup
from typing import List

def get_requirements()-> List[str]:  ##This function will return List Of Requirements

    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            ## Porcess each line
            for line in lines:
                requirement=line.strip()

                ## Ignore Empty ines & - e. 
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("Requirements.txt Is Not Found")


    return requirement_lst

setup(
    name="NetworkSecurity",  ## create new folder having all the packages
    version="0.0.1",
    author="Abdullah",
    author_email="immuhammadabdullah07@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)