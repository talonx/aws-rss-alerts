import feedparser as fp
import argparse
import time


class AWSStatus(object):
    
    OK = 0
    WARNING = 1
    CRITICAL = 2

    def __init__(self):
        self.states = {}
    
    def add_status(self, reg, svc, state, details):
        self.states.get(reg, {})[svc] = (state, details)


class AWSFeedParser(object):

    # Not strictly AWS regions, yet, but more of geo-regions
    REGIONS = ['us', 'ap', 'eu', 'sa']
    STALE_THRESHOLD_SECONDS = 6 * 60 * 60  # 6 hours

    INFORMATIONAL = 'Informational message: '
    SERVICE_NORMAL = 'Service is operating normally: '

    def __init__(self):
        self.regs = {}
        for r in self.REGIONS:
            fname = r + '.txt'
            with open(fname) as f:
                lines = f.readlines()
                self.regs[r] = lines
        # print self.regs

    def _log(self, mes):
        print mes

    # TODO replace this with a dict
    def _wanted(self, svcs, line):
        for svc in svcs:
            if svc in line:
                return True
        return False

    def parse(self, regions=[], svcs=[]):
        for r in regions:
            lines = self.regs[r]
            filtered = [l for l in lines if self._wanted(regions, l)]
            filtered = [l for l in lines if self._wanted(svcs, l)]
            print filtered
            for line in lines:
                for svc in svcs:
                    if svc not in line:
                        continue
                    print "Getting feed for", line
                    feed = fp.parse(line)
                    if 'entries' not in feed:
                        self._log("Empty feed")
                        continue
                    entries = feed['entries']
                    if len(entries) == 0:
                        self._log("Empty feed")
                        continue
                    # published_parsed is in UTC
                    lastpubtime = time.mktime(entries[0]['published_parsed'])
                    curtime = time.mktime(time.gmtime())
                    diff = curtime - lastpubtime
                    if diff > self.STALE_THRESHOLD_SECONDS:
                        self._log("Old entries present")
                        continue
                    for entry in feed['entries']:
                        self._log(entry['title'])
                        pubtime = time.mktime(entry['published_parsed'])
                        curtime = time.mktime(time.gmtime())
                        self._log("Found something")
                    print "-----------------------"


def main():
    parser = argparse.ArgumentParser(description='Process the region and service names')
    parser.add_argument('--regions', help="comma separated list of region names - us, eu, ap, sa")
    parser.add_argument('--services', help="comma separated list of service names - ec2, s3 etc")
    args = parser.parse_args()
    regs = args.regions.split(',')
    svcs = args.services.split(',')
    p = AWSFeedParser()
    p.parse(regs, svcs)

if __name__ == '__main__':
    main()
