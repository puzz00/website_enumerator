#!/usr/bin/python3

# a class which contains methods for enumerating websites

import requests
import subprocess

class DDigger:
    # use a constructor to define what is needed for the class to work
    def __init__(self, target_url, passed_wordlist):
        self.dirs = []
        self.dns_a = []
        self.sd_list = []
        self.url = target_url
        self.wordlist = passed_wordlist

    def fetch_response(self, url):
        # tries to connect to the given URL
        # returns a None type if no connection can be made
        try:
            return requests.get(url)
        except:
            pass

    def get_ip(self, url):
        # uses the subprocess run method to run a dig command in order to retrieve A records
        if url[4] == "s":
            ip_url = url[8:]
        elif url[4] == ":":
            ip_url = url[7:]
        command = "dig +cmd {} +noall +answer".format(ip_url)
        response = subprocess.run(command, capture_output=True,
                                  text=True, shell=True)
        return response.stdout

    def find_directories(self, url):
        # clears the list of discovered directories just in case this method is called more than once
        self.dirs.clear()
        # tries every word in the given directory wordlist as a directory
        # adds any valid directory to a list of directories and avoids duplicating them
        with open(self.wordlist, "r") as directories:
            for line in directories:
                directory = line.strip()
                test_url = "{}/{}".format(url, directory)
                result = self.fetch_response(test_url)
                if (result) and (test_url not in self.dirs):
                    self.dirs.append(test_url)
                    print("\n[++] Found directory --> " + test_url)
        return self.dirs

    def find_subdomains(self, url, dns):
        # prepares the URL for addition of the possible subdomain
        # takes into account if the URL is http or https
        if url[4] == "s":
            protocol = "https://"
            domain = url[8:]
        elif url[4] == ":":
            protocol = "http://"
            domain = url[7:]
        else:
            return
        # clears the dns_a list just in case this method is called more than once
        # clears the subdomain list just in case this method is called more than once
        self.dns_a.clear()
        self.sd_list.clear()
        # tries every word in the given subdomain wordlist as a subdomain
        # adds any valid subdomain to a list of subdomains and avoids duplicating them
        with open(self.wordlist, "r") as file:
            for line in file:
                sd = line.strip()
                test_url = "{}{}.{}".format(protocol, sd, domain)
                response = self.fetch_response(test_url)
                if (response) and (test_url not in self.sd_list):
                    self.sd_list.append(test_url)
                    print("\n[++] Found sub-domain --> " + test_url)
                    if dns:
                        # tries to find the DNS A record for each valid subdomain
                        ip = self.get_ip(test_url)
                        self.dns_a.append(ip)
                        print(ip)
        return self.sd_list, self.dns_a
