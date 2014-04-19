
from distutils.core import setup
setup(
    name = "nomit",
    packages = ["nomit"],
    version = "1.0",
    description = "Process Monit HTTP/XML",
    author = "Markus Juenemann",
    author_email = "markus@juenemann.net",
    url = "https://github.com/mjuenema/nomit",
    download_url = "https://github.com/mjuenema/nomit/tarball/1.0",
    keywords = ["xml", "Monit", "MMonit"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        ],
    long_description = """\
Nomit is a small library that can be used to process HTTP/XML POST 
requests from Monit* instances. While it is a relatively trivial adaption
of Python's BaseHTTPRequestHandler, it may be useful to multiple 
other projects. For this reason Nomit is registered as its own little
project.

*Monit (http://mmonit.com/monit/) is a free utility for managing Unix systems. 
Multiple Monit instances can be centrally managed by its sister project 
MMonit (http://mmonit.com/monit/#mmonit). Monit communicates with 
MMonit through HTTP/XML POST request.

"""
)
