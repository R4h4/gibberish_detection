import json
import datetime
import pickle


def handler(event, context):
    pickle.load(open('/gib_model.pki', 'rb'))

    data = {
        'output': 'Hello Test',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
