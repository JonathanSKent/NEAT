"""
Connects the program to the AWS Machine Learning Module
"""

import boto3
import config

ml = boto3.client('machinelearning',
                  aws_access_key_id=config.aws_a_k,
                  aws_secret_access_key=config.aws_s_a_k,
                  region_name=config.aws_reg)

#Given a list of thirty percent changes as strings, returns a prediction as a float
def nPred(i):
    response = ml.predict(
            MLModelId=config.mlmodid,
            Record={'Point_'+str(x+1):i[x] for x in range(30)},
            PredictEndpoint=config.mlep
            )
    return(response['Prediction']['predictedValue'])