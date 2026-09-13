from networkSecurity.entity.artifact_entity import ClassificationMetricsArtifact
from networkSecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score
from networkSecurity.exception.exception import NetworkSecurityException
import sys


def get_classificiation_score(y_true,y_pred)->ClassificationMetricsArtifact:
    try:
        model_f1_score=f1_score(y_true,y_true)
        model_precision_score=precision_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)

        classification_metrics_artifact=ClassificationMetricsArtifact(f1_score=model_f1_score,
                                      precision_score=model_precision_score,
                                      recall_score=model_recall_score)
        return classification_metrics_artifact
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)