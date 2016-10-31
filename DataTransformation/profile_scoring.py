import csv
import datetime
from pymongo import MongoClient
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
import functools



DEFAULT_HOST = "mongo.da.msignia.com"
DEFAULT_PORT = 27017
DEFAULT_DB = "msignia"
DEFAULT_COLLECTION = "raw_transactions"


failed_checkins ={}
above_threshold_checkins ={}
mdid_scores={}

sum_false_reject_ratio = 0
sum_false_accept_ratio = 0
counter = 0
total_number_of_false_rejects =0
total_number_of_checkins = 0
total_number_of_false_accepts = 0
total_number_of_imposter = 0
total_number_of_imposter_detected =0
f = open('report_300','w')
THRESHOLD =75


def retrieve_scores(mdid):
    client = MongoClient(DEFAULT_HOST, DEFAULT_PORT)
    db = client[DEFAULT_DB]
    collection = db[DEFAULT_COLLECTION]
    collection.ensure_index([("createdAt", pymongo.ASCENDING)])
    query = collection.find({"scoreStats.issuedScore": {'$exists': "true"}, "transactionStats.mdid": mdid},
                            {"scoreStats": 1, "_id": 0, "createdAt": 1, "transactionStats": 1, })

    global mdid_scores, failed_checkins, above_threshold_checkins
    mdid_scores[mdid] = []
    failed_checkins[mdid] =[]
    above_threshold_checkins[mdid]=[]

    for result in query:

        item = (result['createdAt'], float(result['scoreStats']['issuedScore']), result['transactionStats']['platform'])
        mdid_scores[mdid].append(item)
        if item[1] < THRESHOLD:
            failed_checkins[mdid].append(item)
        else:
            above_threshold_checkins[mdid].append(item)

    # return mdid_scores


def get_mdid_list():
    client = MongoClient(DEFAULT_HOST, DEFAULT_PORT)
    db = client[DEFAULT_DB]
    collection = db[DEFAULT_COLLECTION]
    query = collection.distinct('transactionStats.mdid')
    mdid_list = list(query)
    client.close()
    return mdid_list


"""
    this method takes in the mdid and distinct created at time stamp and finds the ones which are genuine checkins
    the imposter label tells if we need to see the imposter(imposter = true) or genuine (imposter = false)

"""

def imposter_present(mdid, createdAt_list, imposter):
    client = MongoClient(DEFAULT_HOST, DEFAULT_PORT)
    db = client[DEFAULT_DB]
    collection = db["checkin_details"]
    queries = collection.distinct("createdAt",{"mdid": str(mdid), "createdAt":{'$in': createdAt_list}, "imposter":imposter})
    # print(queries)
    return len(queries)

def parallel_process(md):
    false_reject_ratio = 0
    retrieve_scores(md)
    q = above_threshold_checkins[md]
    q2 = failed_checkins[md]
    q = [x[0] for x in q]
    q2 =[x[0] for x in q2]

    total_profile_checkins = len(set(q)) + len(set(q2))
    imposter_checkins = imposter_present(md, q, True)
    false_reject = imposter_present(md, q2, False)

    """
    total_number_of_false_rejects is for all the profiles combined it is different from sum which will be used to calculate
    the average rate of false reject
    """

    global total_number_of_imposter_detected, total_number_of_false_accepts, total_number_of_false_rejects,total_number_of_checkins
    total_number_of_imposter_detected += imposter_present(md,q2, True)
    total_number_of_false_accepts += imposter_checkins
    total_number_of_false_rejects += false_reject
    total_number_of_checkins += total_profile_checkins

    false_accept_ratio = imposter_checkins/total_profile_checkins
    false_reject_ratio = false_reject/total_profile_checkins

    global sum_false_reject_ratio, sum_false_accept_ratio, counter

    sum_false_reject_ratio += false_reject_ratio
    sum_false_accept_ratio += false_accept_ratio

    """
    assigning to empty to reduce space usuage.
    """
    del above_threshold_checkins[md]
    del failed_checkins[md]
    str_= str(md)+ "\t" + str(false_reject_ratio) + " \t" + str(false_accept_ratio)

    global f
    f.write(str_)
    print(str_)
    counter += 1



def main():
    current = datetime.datetime.now()
    mdid_list = get_mdid_list()
    pool = ThreadPool(4)
    # results = pool.map(retrieve_scores, mdid_list)
    results = pool.map(parallel_process, mdid_list)
    str_ = "\tfalse reject "+ str(sum_false_reject_ratio/counter)+"\nfalse reject ratio across all profiles\t"+str(total_number_of_false_rejects/total_number_of_checkins)+"\tfalse accept\t"+str(total_number_of_false_accepts/total_number_of_checkins)
    print(str_)
    global f
    f.write(""+str(datetime.datetime.now()) +"\n"+ str_)
    f.close()
    print((current - datetime.datetime.now()).total_seconds())
main()