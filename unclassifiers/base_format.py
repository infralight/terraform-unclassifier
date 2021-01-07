from abc import abstractmethod
from unclassifiers.config import Config


class BaseFormat:

    def __init__(self, config: Config):
        self.config = config
        self.legitimate_fields = ["arn", "id", "owner_id", "vpc_id", "domain_name"]

    @abstractmethod
    def unclassify(self, tf_state_file):
        pass