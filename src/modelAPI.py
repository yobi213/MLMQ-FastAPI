import requests
import config as cfg


class ModelAPI:

    def __init__(self):
        self.model_url = cfg.model_url

    def get_model_pred(self,sentence):

        pred = requests.get(self.model_url+sentence).json()

        return pred

#
#
# modelAPI = ModelAPI()
# print(modelAPI.get_model_pred('배송이 빨라서 좋아요'))