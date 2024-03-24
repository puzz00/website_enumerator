# website_enumerator
Seeks to find subdomains and directories.

I wrote this as I enjoy using tools such as Gobuster and Dirb so I wanted to have a go at making my own Pythonic version of them. This one needs to be run off a command line.

Flags:

- `-u` specify the target domain for example `https://targetdomain.com`
- `-w` specify a wordlist - there is a default in the code but the path could be different on different operating systems
- `-d` get the program to try to find directories
- `-s` get the program to try to find subdomains
- `-a` get the DNS A Records for the found subdomains (needs dig to be installed on the system - already installed on Parrot and Kali)
- `-h` shows help

Basic usage example:

`python ddigger.py -u https://www.tesla.com -w /usr/share/dirb/wordlists/common.txt -d -s`
