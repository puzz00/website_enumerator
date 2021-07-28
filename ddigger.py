#!usr/bin/python3

# domain digger (ddigger) by puz00

# instantiates a ddigger object which allows a user to enumerate a domain
# -u flag for URL
# -w flag for wordlist to find subdomains if needed
# will use the default path /usr/share/dirb/wordlists/common.txt if -w not specified by the user
# this will work on Parrot OS but perhaps not others
# it is therefore best to specify a wordlist you know exists on your OS
# -d flag to find directories
# -s flag to find subdomains
# -a flag to retrieve DNS A Records (needs dig to be installed for this option to work)

from ddigger_class import DDigger
import optparse

# main
# instantiates an OptionParser object and uses it to set up command line options
parser = optparse.OptionParser()
parser.add_option("-u", "--url", action="store", dest="url",
                  help="Target domain in scope - for example https://domain.com")
parser.add_option("-w", "--wordlist", action="store", dest="wordlist",
                  help="Path to wordlist for finding subdomains - eg /home/user/words.txt")
parser.add_option("-s", "--subdomains", action="store_true", dest="subdomains",
                  help="Use -s if you would like to try to find subdomains",
                  default=False)
parser.add_option("-d", "--directories", action="store_true", dest="directories",
                  help="Use -d to try to find directories",
                  default=False)
parser.add_option("-a", "--arecords", action="store_true", dest="arecords",
                  help="Use -a to try to find DNS A Records (needs dig to be installed)",
                  default=False)

options, args = parser.parse_args()

# let the user know they need to specify a target domain if they do not do so
if not options.url:
    print("\n[**] Specify a target domain with the -u flag - for example -u https://domain.com")
    print("\n[**] Example of usage to find directories and subdomains for google...")
    print("\npython ddigger.py -u https://google.com -d -s\n")
    exit()

# create a variable to work with which uses the given URL
url = ""
url += options.url

if options.wordlist:
    # creates a wordlist to work with from the given wordlist
    wordlist = ""
    wordlist += options.wordlist
else:
    # creates a default wordlist to work with
    wordlist = ""
    wordlist += "/home/win10/words.txt"

# instantiates a DDigger object
digger = DDigger(url, wordlist)

if options.directories:
    # tries to find directories if the user specifies this with the -d flag
    print("\n\n[**] Trying to find directories...")
    dirs = digger.find_directories(url)
    if len(dirs) > 0:
        print("\n\n[++] The following directories are valid:\n\n")
        i = 1
        for directory in dirs:
            print("{}\t{}".format(i, directory))
            i += 1
    else:
        print("\n\n[!!] No valid directories found!")

if options.subdomains:
    # tries to find subdomains if the user specifies this with the -s flag
    print("\n\n[**] Trying to find subdomains...")
    if options.arecords:
        found_subdomains, a_records = digger.find_subdomains(url, True)
    else:
        found_subdomains, a_records = digger.find_subdomains(url, False)
    if len(found_subdomains) > 0:
        print("\n\n[++] The following subdomains are valid:\n\n")
        i = 1
        for sd in found_subdomains:
            print("{}:\t{}".format(i, sd))
            i += 1
        print("\n\n[++] Here are their DNS A Records:\n\n")
        for a in a_records:
            print(a)
    else:
        print("\n\n[!!] No valid subdomains found!")
