import feedparser as fp
import sys

class AWSFeedParser(object):
    
    ## Not strictly AWS regions, yet, but more of geo-regions
    REGIONS = ['us', 'ap', 'eu', 'sa']

    def __init__(self):
        self.regs = {}
        for r in self.REGIONS:
            fname = r + '.txt'
            with open(fname) as f:
                lines = f.readlines()
                self.regs[r] = lines
        
        print self.regs


    ## TODO replace this with a dict
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
                    for entry in feed['entries']:
                        print entry['title']
                    print "-----------------------"


def main():
    p = AWSFeedParser()
    regs = ['eu']
    svcs = ['ec2', 's3']
    p.parse(regs, svcs)

if __name__ == '__main__':
    main()
