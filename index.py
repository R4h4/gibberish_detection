#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pickle
import math


def handler(event, context):

    req_name = event['queryStringParameters']['string']

    model_data = pickle.load(open('./gib_model.pki', 'rb'))

    accepted_chars = 'abcdefghijklmnopqrstuvwxyzöäüèéáıçğ-ßó '
    pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])

    def normalize(line):
        return [c.lower() for c in line if c.lower() in accepted_chars]

    def ngram(n, l):
        # Return all n grams from l after normalizing
        filtered = normalize(l)
        for start in range(0, len(filtered) - n + 1):
            yield ''.join(filtered[start:start + n])

    def avg_transition_prob(l, log_prob_mat):
        # Return the average transition prob from l through log_prob_mat.
        log_prob = 0.0
        transition_ct = 0
        for a, b in ngram(2, l):
            log_prob += log_prob_mat[pos[a]][pos[b]]
            transition_ct += 1
        # The exponentiation translates from log probs to probs.
        return math.exp(log_prob / (transition_ct or 1))

    def gibberish(name):
        model_mat = model_data['mat']
        threshold = model_data['thresh']
        return avg_transition_prob(name, model_mat) < threshold

    res = gibberish(req_name)

    data = {
        'string': req_name,
        'gibberish': res
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
