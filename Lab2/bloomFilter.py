import pandas as pd
import math
from random import shuffle
import mmh3 
from bitarray import bitarray 

class BloomFilter(object):
    def init(self, arrLen, n):
        self.arrLen = arrLen
        self.n = n
        self.noOfHash = BloomFilter.hashMapReq(arrLen, n)
        self.arr = bitarray(arrLen)
        self.arr.setall(0)

    def hashMapReq(m, n):
        return int((m/n)*math.log(2))

    def findDigest(self, str):
        digest = []
        for i in range(self.noOfHash):
            idx = mmh3.hash(str) % self.arrLen
            digest.append(idx)
        return digest

    def insert(self, str):
        digest = self.findDigest(str)
        self.arr[digest] = True

    def isPresent(self, str):
        digest = self.findDigest(str)
        return all(self.arr[d] for d in digest)

def main():
    # Read the CSV file
    df = pd.read_csv('spam_or_not_spam.csv')

    # Initialize Bloom Filter
    arrLen = 100000  # Adjust the array length based on your dataset size
    n = len(df[df['label'] == 0])  # Number of non-spam emails
    bloomf = BloomFilter(arrLen, n)

    # Insert non-spam emails into the Bloom Filter
    non_spam_emails = df[df['label'] == 0]['email'].tolist()
    for email in non_spam_emails:
        bloomf.insert(email)

    # Test the Bloom Filter with some spam emails
    test_emails = df[df['label'] == 1]['email'].sample(n=10).tolist()
    for email in test_emails:
        if bloomf.isPresent(email):
            print("'{}' is probably not spam.".format(email))
        else:
            print("'{}' might be spam.".format(email))


main()