import setuptools
import shutil
from setuptools.command.sdist import sdist

#Cleanup before sdist
class CustomSdist(sdist):
    def run(self):
        shutil.rmtree("dist")
        sdist.run(self)


#Package
setuptools.setup(
    name="SignalProcessing",
    version="1.0.0",
    author="Oliver Bründler",
    author_email="oliver.bruendler@psi.ch",
    description="Signal processing development helpers",
    url="https://git.psi.ch/GFA/Libraries/Firmware/Python/SignalProcessing",
    packages=setuptools.find_packages(),
    install_requires = [
        "scipy",
        "matplotlib",
        "numpy",
        "typing"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    cmdclass = {
        "sdist" : CustomSdist
    }
)